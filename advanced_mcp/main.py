from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth.providers.jwt import JWTVerifier

import os

load_dotenv()

auth = JWTVerifier(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json",
    issuer=os.getenv('STYTCH_DOMAIN'),
    algorithm='RS256',
    audience=os.getenv('STYTCH_PROJECT_ID')
)

mcp = FastMCP(name="Notes App", auth=auth)

NOTES_FILE = "notes.txt"


def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky notes file.

    Args:
        message(str): The note content to be added.

    Returns:
        str: confirmation message indicating the note has been added.
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return f'Saved note: "{message}"'

@mcp.tool()
def read_notes() -> str:
    """
    Read all notes from the sticky notes file.

    Returns:
        str: A string containing all notes, separated by newlines.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()

    return content or "No notes yet!"

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the sticky notes file.

    Returns:
        str: The latest note, or "No notes yet!" if the file is empty.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.readlines()
    return content[-1].strip() if content else "No notes yet!"

@mcp.prompt()
def note_summary_prompt() -> str:
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()

    if not content:
        return "No notes yet!"

    return f"""
    You are a helpful assistant that summarizes sticky notes.
    The notes are:
    {content}
    """

@mcp.custom_route('/.well-known/oauth-protected-resource', methods=["GET", "OPTIONS"])
def oauth_protected_resource(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )

@mcp.custom_route('/.well-known/oauth-protected-resource/mcp', methods=["GET", "OPTIONS"])
def oauth_protected_resource_mcp(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )

@mcp.custom_route('/.well-known/oauth-authorization-server', methods=["GET", "OPTIONS"])
def oauth_authorization_server(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )

@mcp.custom_route('/.well-known/openid-configuration', methods=["GET", "OPTIONS"])
def openid_configuration(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
        ]
    )
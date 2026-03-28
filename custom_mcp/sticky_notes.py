from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("sticky_notes")

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


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
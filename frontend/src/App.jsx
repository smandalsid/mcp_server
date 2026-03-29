import { StytchLogin, IdentityProvider, useStytchUser, Products, OTPMethods } from "@stytch/react"

function App() {
  const { user } = useStytchUser();

  // Must exactly match a URL in Stytch Dashboard → Redirect URLs (same scheme, host, port, path).
  const redirectURL =
    import.meta.env.VITE_STYTCH_REDIRECT_URL || window.location.origin;

    const config = {
      products: [Products.otp],
      otpOptions: {
        methods: [OTPMethods.Email],
        expirationMinutes: 10,
      },
      sessionOptions: {
        sessionDurationMinutes: 60,
      },
    };
    
    const presentation = {
      theme: [
        {
            "font-family": "Rockwell, 'Rockwell Nova', 'Roboto Slab', 'DejaVu Serif', 'Sitka Small', serif",
            "font-family-mono": "ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'DejaVu Sans Mono', monospace",
            "spacing": "4px",
            "rounded-base": "4px",
            "text-base": "1rem",
            "container-width": "400px",
            "mobile-breakpoint": "768px",
            "transition-duration": "0.15s",
            "destructive-foreground": "#ffffff",
            "color-scheme": "light",
            "background": "#ffffff",
            "container-border": "#e5e7eb",
            "foreground": "#111827",
            "primary": "#d87943",
            "primary-foreground": "#ffffff",
            "secondary": "#527575",
            "secondary-foreground": "#ffffff",
            "muted": "#f3f4f6",
            "muted-foreground": "#6b7280",
            "accent": "#5f8787",
            "accent-foreground": "#ffffff",
            "border": "#e5e7eb",
            "input": "#e5e7eb",
            "ring": "#d87943",
            "destructive": "#ef4444",
            "warning": "#f97316",
            "success": "#5f8787",
            "shadow": "rgba(0, 0, 0, 0.05) 0px 1px 4px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px -1px"
        },
        {
            "font-family": "Rockwell, 'Rockwell Nova', 'Roboto Slab', 'DejaVu Serif', 'Sitka Small', serif",
            "font-family-mono": "ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'DejaVu Sans Mono', monospace",
            "spacing": "4px",
            "rounded-base": "4px",
            "text-base": "1rem",
            "container-width": "400px",
            "mobile-breakpoint": "768px",
            "transition-duration": "0.15s",
            "destructive-foreground": "#ffffff",
            "color-scheme": "dark",
            "background": "#121212",
            "container-border": "#222222",
            "foreground": "#c1c1c1",
            "primary": "#e78a53",
            "primary-foreground": "#121113",
            "secondary": "#5f8787",
            "secondary-foreground": "#121113",
            "muted": "#1a1a1a",
            "muted-foreground": "#888888",
            "accent": "#5f8787",
            "accent-foreground": "#ffffff",
            "border": "#222222",
            "input": "#222222",
            "ring": "#e78a53",
            "destructive": "#ef4444",
            "warning": "#f97316",
            "success": "#5f8787"
        },
      ],
      options: {},
    };

  return (
    <div>
      {!user ? <StytchLogin config={config} presentation={presentation} /> : <IdentityProvider />}
    </div>
  )
}

export default App

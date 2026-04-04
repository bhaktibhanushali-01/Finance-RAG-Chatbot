import os
import re

print("Starting UI rewrite...")

# 1. Update index.css
css_path = os.path.join('frontend', 'src', 'index.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace RGBs
css = css.replace('139,92,246', '212,175,55')
css = css.replace('139, 92, 246', '212, 175, 55')
css = css.replace('59,130,246', '170,136,37')
css = css.replace('59, 130, 246', '170, 136, 37')

# Replace root
root_pattern = r':root\s*\{.*?\n\}'
new_root = """:root {
  /* Core palette - Obsidian */
  --bg-primary:   #030303;
  --bg-secondary: #0a0a0a;
  --bg-tertiary:  #111111;
  --bg-card:      rgba(10, 10, 10, 0.45);
  --bg-glass:     rgba(255, 255, 255, 0.02);

  /* Accent - Champagne Gold */
  --accent-gold:    #D4AF37;
  --accent-gold-light: #F3E5AB;
  --accent-gold-dark: #aa8825;
  --accent-cyan:    #06b6d4;
  --accent-green:   #10b981;
  --accent-red:     #ef4444;

  --accent-purple:  var(--accent-gold);
  --accent-blue:    var(--accent-gold-dark);

  /* Gradient */
  --gradient-brand: linear-gradient(135deg, #aa8825 0%, #D4AF37 50%, #F5E8A6 100%);
  --gradient-card:  linear-gradient(135deg, rgba(212,175,55,0.08) 0%, rgba(212,175,55,0.01) 100%);
  --gradient-glow:  radial-gradient(circle at 50% 50%, rgba(212,175,55,0.2) 0%, transparent 50%);

  /* Text - High Contrast */
  --text-primary:   #ffffff;
  --text-secondary: #e5e5e5;
  --text-muted:     #737373;
  --text-accent:    var(--accent-gold-light);

  /* Borders - Sharper & Glassier */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-hover:  rgba(212, 175, 55, 0.4);

  /* Shadows - Deeper */
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.6);
  --shadow-md:  0 4px 16px rgba(0,0,0,0.8);
  --shadow-lg:  0 12px 40px rgba(0,0,0,0.9);
  --shadow-glow: 0 0 30px rgba(212,175,55,0.15);

  /* Radii */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4,0,0.2,1);
  --transition-normal: 250ms cubic-bezier(0.4,0,0.2,1);
  --transition-slow: 400ms cubic-bezier(0.4,0,0.2,1);

  /* Layout */
  --sidebar-width: 340px;
  --header-height: 64px;
}"""
css = re.sub(root_pattern, new_root, css, flags=re.DOTALL)

# Replace app-layout::before with Aurora classes
old_glow = r"""/\* Ambient glow \*/\s*\.app-layout::before\s*\{.*?\}"""

aurora_css = """/* ---------- 3D Aurora Mesh Gradient ---------- */
.aurora-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background: var(--bg-primary);
}

.aurora-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  opacity: 0.5;
  animation: floatOrb 20s infinite alternate ease-in-out;
  will-change: transform;
}

.aurora-orb-1 {
  width: 65vw;
  height: 65vw;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.12) 0%, transparent 60%);
  top: -25vh;
  left: -25vw;
  animation-duration: 25s;
}

.aurora-orb-2 {
  width: 55vw;
  height: 55vw;
  background: radial-gradient(circle, rgba(170, 136, 37, 0.1) 0%, transparent 60%);
  bottom: -25vh;
  right: -15vw;
  animation-delay: -5s;
  animation-duration: 22s;
  animation-direction: alternate-reverse;
}

.aurora-orb-3 {
  width: 45vw;
  height: 45vw;
  background: radial-gradient(circle, rgba(243, 229, 171, 0.08) 0%, transparent 60%);
  top: 30vh;
  left: 30vw;
  animation-delay: -10s;
  animation-duration: 18s;
}

@keyframes floatOrb {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  33% { transform: translate(6vw, 6vh) scale(1.1) rotate(10deg); }
  66% { transform: translate(-6vw, 10vh) scale(0.9) rotate(-10deg); }
  100% { transform: translate(0, -6vh) scale(1.05) rotate(5deg); }
}"""

css = re.sub(old_glow, aurora_css, css, flags=re.DOTALL)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated index.css")

# 2. Update App.jsx
app_path = os.path.join('frontend', 'src', 'App.jsx')
with open(app_path, 'r', encoding='utf-8') as f:
    app_jsx = f.read()

aurora_jsx = """    <div className="app-layout">
      <div className="aurora-container">
        <div className="aurora-orb aurora-orb-1"></div>
        <div className="aurora-orb aurora-orb-2"></div>
        <div className="aurora-orb aurora-orb-3"></div>
      </div>
"""

app_jsx = app_jsx.replace('<div className="app-layout">', aurora_jsx)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_jsx)
print("Updated App.jsx")

print("UI rewrite completed successfully!")

<div align="center">

![TEZERE Banner](https://via.placeholder.com/1200x300/0a0a2e/ffffff?text=TEZERE+-+Cyber+Dev+Portfolio)

# TEZERE - Portfolio Développeur Fullstack & Architecte CyberSécurité
**teano-cevalier** | Loudun, Nouvelle-Aquitaine, FR | *MàJ: 06/03/2026*

[![GitHub followers](https://img.shields.io/github/followers/teano-cevalier?label=Followers&style=social)](https://github.com/teano-cevalier)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*Live Demo : [studio.r00ting.xyz](http://127.0.0.1:5001)*

</div>

## 🚀 À propos de ce Portfolio
Ce portfolio TEZERE est une app web fullstack Flask showcaseant mes skills en dev, sysadmin (Proxmox/Pterodactyl) et cybersécu. Thème cyberpunk : grid canvas interactif (mousemove glow), animations AOS fluides, responsive mobile-first avec JetBrains Mono. Protection anti-DoS via Flask-Limiter et headers CSP.[cite:1][cite:4]

- **Objectif** : Attirer recruteurs/clients pour hosting Minecraft, infra sécurisée, pentest légal.
- **Inspirations** : Cyberpunk 2077 + hacker folios pros.[web:10][web:13]

## 💻 Le Code Explicité
Source open : Flask/Python backend + HTML/CSS/JS vanilla frontend. Pas de frameworks lourds pour perf max.

```mermaid
graph TD
    A[Flask App] --> B[Routes / Render Templates]
    A --> C[Flask-Limiter Rate Limit]
    B --> D[Canvas Grid Interactif JS]
    B --> E[AOS Animations + Observers]
    C --> F[CSP Headers Sécurité]
    D --> G[JetBrains Mono Responsive]


import os
import secrets
from datetime import datetime
from flask import Flask, render_template_string, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TEZERE | Développement & sysadmin</title>
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #00ff9d;
            --primary-dark: #00cc7d;
            --bg: #0a0a0a;
            --bg-light: #111111;
            --bg-lighter: #1a1a1a;
            --text: #ffffff;
            --text-dim: #888888;
            --border: #222222;
            --glow: rgba(0, 255, 157, 0.2);
        }

        body {
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }

        canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        nav {
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(10, 10, 10, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            z-index: 100;
            padding: 1rem 0;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary);
            text-shadow: 0 0 15px var(--glow);
        }

        .nav-links {
            display: flex;
            gap: 2rem;
        }

        .nav-links a {
            color: var(--text);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: var(--primary);
        }
        section {
            position: relative;
            z-index: 1;
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding: 6rem 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        #hero {
            text-align: center;
        }

        .hero-title {
            font-size: 5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            line-height: 1.2;
            color: var(--primary);
            text-shadow: 0 0 30px var(--primary);
            animation: glow 3s infinite;
        }

        @keyframes glow {
            0%, 100% { text-shadow: 0 0 20px var(--primary); }
            50% { text-shadow: 0 0 40px var(--primary); }
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: var(--text-dim);
            margin-bottom: 2rem;
            letter-spacing: 4px;
        }

        .hero-tags {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            max-width: 800px;
            margin: 0 auto;
        }

        .hero-tag {
            padding: 0.5rem 1.2rem;
            background: rgba(0, 255, 157, 0.05);
            border: 1px solid var(--primary);
            border-radius: 50px;
            font-size: 0.9rem;
            color: var(--primary);
            transition: all 0.3s;
        }

        .hero-tag:hover {
            background: var(--primary);
            color: var(--bg);
            transform: scale(1.1);
        }

</div>
        .about-content {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }

        .about-text {
            color: var(--text-dim);
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 3rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin: 4rem 0;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-dim);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* Skills Section */
        #skills {
            background: rgba(0, 0, 0, 0.7);
        }

        .section-title {
            font-size: 2.5rem;
            margin-bottom: 3rem;
            position: relative;
            color: var(--primary);
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 60px;
            height: 4px;
            background: var(--primary);
            box-shadow: 0 0 20px var(--primary);
        }

        .skills-category {
            margin-bottom: 3rem;
        }

        .category-title {
            font-size: 1.3rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .category-title i {
            font-size: 1.5rem;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .skill-card {
            background: var(--bg-light);
            border: 1px solid var(--border);
            padding: 1.5rem;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        .skill-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 157, 0.1), transparent);
            transition: left 0.5s;
        }

        .skill-card:hover::before {
            left: 100%;
        }

        .skill-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px var(--glow);
        }

        .skill-icon {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }

        .skill-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .skill-level {
            height: 4px;
            background: var(--border);
            border-radius: 2px;
            overflow: hidden;
        }

        .skill-level-bar {
            height: 100%;
            background: var(--primary);
            width: 0;
            transition: width 1s;
        }

        .skill-card:hover .skill-level-bar {
            width: attr(data-level);
        }

        /* Projects Section */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
        }

        .project-card {
            background: var(--bg-light);
            border: 1px solid var(--border);
            padding: 2rem;
            transition: all 0.3s;
        }

        .project-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px var(--glow);
        }

        .project-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .project-icon {
            width: 60px;
            height: 60px;
            background: rgba(0, 255, 157, 0.1);
            border: 1px solid var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            color: var(--primary);
        }

        .project-title h3 {
            font-size: 1.3rem;
            margin-bottom: 0.3rem;
        }

        .project-date {
            color: var(--text-dim);
            font-size: 0.8rem;
        }

        .project-desc {
            color: var(--text-dim);
            margin-bottom: 1.5rem;
            line-height: 1.7;
        }

        .project-tech {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .project-tech span {
            background: rgba(0, 255, 157, 0.05);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 0.3rem 0.8rem;
            font-size: 0.75rem;
        }

        /* Architecture Section */
        #architecture {
            background: rgba(0, 0, 0, 0.7);
        }

        .arch-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
        }

        .arch-card {
            background: var(--bg-light);
            border: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s;
        }

        .arch-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
        }

        .arch-icon {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
        }

        .arch-card h4 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }

        .arch-card p {
            color: var(--text-dim);
            font-size: 0.9rem;
        }

        /* Contact Section */
        .contact-container {
            max-width: 600px;
            margin: 0 auto;
            background: var(--bg-light);
            border: 1px solid var(--border);
            padding: 3rem;
            text-align: center;
        }

        .contact-email {
            font-size: 1.5rem;
            color: var(--primary);
            margin: 2rem 0;
            font-family: monospace;
        }

        .contact-social {
            display: flex;
            justify-content: center;
            gap: 2rem;
        }

        .contact-social a {
            color: var(--text-dim);
            font-size: 2rem;
            transition: all 0.3s;
        }

        .contact-social a:hover {
            color: var(--primary);
            transform: translateY(-5px);
        }
        footer {
            position: relative;
            z-index: 1;
            padding: 2rem;
            text-align: center;
            border-top: 1px solid var(--border);
            color: var(--text-dim);
            font-size: 0.9rem;
        }
        @media (max-width: 768px) {
            .hero-title {
                font-size: 3rem;
            }
            
            .stats-grid,
            .projects-grid,
            .arch-grid {
                grid-template-columns: 1fr;
            }
            
            .nav-links {
                display: none;
            }
        }

        .fade-up {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s, transform 0.6s;
        }

        .fade-up.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .delay-1 { transition-delay: 0.1s; }
        .delay-2 { transition-delay: 0.2s; }
        .delay-3 { transition-delay: 0.3s; }
        [data-aos] {
            pointer-events: none;
        }
        [data-aos].aos-animate {
            pointer-events: auto;
        }
    </style>
</head>
<body>
    <canvas id="grid"></canvas>
    
    <nav>
        <div class="nav-container">
            <div class="logo">TEZERE</div>
            <div class="nav-links">
                <a href="#hero">HOME</a>
                <a href="#skills">COMPÉTENCES</a>
                <a href="#projects">PROJETS</a>
                <a href="#architecture">ARCHITECTURE</a>
                <a href="#contact">CONTACT</a>
            </div>
        </div>
    </nav>
    <section id="hero">
        <div class="container">
            <div class="hero-title fade-up">TEZERE</div>
            <div class="hero-subtitle fade-up delay-1">DÉVELOPPEUR & sysadmin</div>
            <div class="hero-tags fade-up delay-2">
                <span class="hero-tag">#Java</span>
                <span class="hero-tag">#Python</span>
                <span class="hero-tag">#Docker</span>
                <span class="hero-tag">#MongoDB</span>
                <span class="hero-tag">#PostgreSQL</span>
            </div>
        </div>
    </section>
    <section id="skills">
        <div class="container">
            <h2 class="section-title fade-up" data-aos="fade-up">COMPÉTENCES TECHNIQUES</h2>
            
            <div class="skills-category fade-up" data-aos="fade-up" data-aos-delay="100">
                <div class="category-title">
                    <i class="fas fa-code"></i>
                    <span>Langages & Frameworks</span>
                </div>
                <div class="skills-grid">
                    <div class="skill-card" data-level="90" data-aos="flip-left" data-aos-delay="150">
                        <div class="skill-icon"><i class="fab fa-java"></i></div>
                        <div class="skill-name">Java</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 90%"></div></div>
                    </div>
                    <div class="skill-card" data-level="85" data-aos="flip-left" data-aos-delay="200">
                        <div class="skill-icon"><i class="fab fa-python"></i></div>
                        <div class="skill-name">Python</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 85%"></div></div>
                    </div>
                    <div class="skill-card" data-level="40" data-aos="flip-left" data-aos-delay="250">
                        <div class="skill-icon"><i class="fab fa-js"></i></div>
                        <div class="skill-name">JavaScript/TypeScript</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 40%"></div></div>
                    </div>
                    <div class="skill-card" data-level="80" data-aos="flip-left" data-aos-delay="300">
                        <div class="skill-icon"><i class="fab fa-react"></i></div>
                        <div class="skill-name">React/Node.js</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 80%"></div></div>
                    </div>
                    <div class="skill-card" data-level="4" data-aos="flip-left" data-aos-delay="350">
                        <div class="skill-icon"><i class="fab fa-angular"></i></div>
                        <div class="skill-name">Angular</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 4%"></div></div>
                    </div>
                </div>
            </div>
            <div class="skills-category fade-up" data-aos="fade-up" data-aos-delay="200">
                <div class="category-title">
                    <i class="fas fa-database"></i>
                    <span>Bases de données</span>
                </div>
                <div class="skills-grid">
                    <div class="skill-card" data-level="85" data-aos="zoom-in" data-aos-delay="250">
                        <div class="skill-icon"><i class="fas fa-database"></i></div>
                        <div class="skill-name">PostgreSQL</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 85%"></div></div>
                    </div>
                    <div class="skill-card" data-level="80" data-aos="zoom-in" data-aos-delay="300">
                        <div class="skill-icon"><i class="fas fa-database"></i></div>
                        <div class="skill-name">MongoDB</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 80%"></div></div>
                    </div>
                    <div class="skill-card" data-level="75" data-aos="zoom-in" data-aos-delay="350">
                        <div class="skill-icon"><i class="fas fa-database"></i></div>
                        <div class="skill-name">MySQL</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 75%"></div></div>
                    </div>
                    <div class="skill-card" data-level="70" data-aos="zoom-in" data-aos-delay="400">
                        <div class="skill-icon"><i class="fas fa-database"></i></div>
                        <div class="skill-name">Redis</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 70%"></div></div>
                    </div>
                </div>
            </div>

            <div class="skills-category fade-up" data-aos="fade-up" data-aos-delay="300">
                <div class="category-title">
                    <i class="fas fa-cloud"></i>
                    <span>DevOps & Cloud</span>
                </div>
                <div class="skills-grid">
                    <div class="skill-card" data-level="80" data-aos="fade-right" data-aos-delay="350">
                        <div class="skill-icon"><i class="fab fa-docker"></i></div>
                        <div class="skill-name">Docker</div>
                        <div class="skill-level"><div class="skill-level-bar" style="width: 80%"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects">
        <div class="container">
            <h2 class="section-title fade-up" data-aos="fade-up">PROJETS</h2>
            
<div class="projects-grid">
    <div class="project-card fade-up" data-aos="fade-right" data-aos-delay="100">
        <div class="project-header">
            <div class="project-icon"><i class="fas fa-crown"></i></div>
            <div class="project-title">
                <h3>MINETOST STUDIO</h3>
                <div class="project-date">2025 • Lancé</div>
            </div>
        </div>
        <p class="project-desc">
            Studio de développement et de création. Infrastructure complète pour la gestion de projets créatifs et le développement d'applications.
        </p>
        <div class="project-tech">
            <span>Studio</span>
            <span>Création</span>
            <span>Développement</span>
            <span>Infrastructure</span>
        </div>
    </div>

    <div class="project-card fade-up" data-aos="fade-left" data-aos-delay="200">
        <div class="project-header">
            <div class="project-icon"><i class="fas fa-shield"></i></div>
            <div class="project-title">
                <h3>ROOT TEAM</h3>
                <div class="project-date">2026 • Actif</div>
            </div>
        </div>
        <p class="project-desc">
            Équipe spécialisée dans la gestion et la sécurité. Nothing Chat - Application de messagerie 100% sécurisée avec chiffrement de bout en bout et zéro confiance.
        </p>
        <div class="project-tech">
            <span>Nothing Chat</span>
            <span>100% Sécurisé</span>
            <span>Chiffrement</span>
            <span>Zero Trust</span>
        </div>
    </div>
    <div class="project-card fade-up" data-aos="fade-right" data-aos-delay="300">
        <div class="project-header">
            <div class="project-icon"><i class="fas fa-server"></i></div>
            <div class="project-title">
                <h3>2026 STATUS SERVEUR</h3>
                <div class="project-date">2026 • En ligne</div>
            </div>
        </div>
        <p class="project-desc">
            Infrastructure de surveillance et de monitoring de serveurs. Système de statut en temps réel avec alertes et rapports de performance.
        </p>
        <div class="project-tech">
            <span>Monitoring</span>
            <span>Serveurs</span>
            <span>Status</span>
            <span>Alerting</span>
        </div>
    </div>
    <div class="project-card fade-up" data-aos="fade-left" data-aos-delay="400">
        <div class="project-header">
            <div class="project-icon"><i class="fas fa-envelope"></i></div>
            <div class="project-title">
                <h3>JusteMail</h3>
                <div class="project-date">2026 • En développement</div>
            </div>
        </div>
        <p class="project-desc">
            Système de messagerie avancé en cours de développement. Architecture moderne, sécurité renforcée, interface intuitive et fonctionnalités innovantes.
        </p>
        <div class="project-tech">
            <span>En développement</span>
            <span>Messagerie</span>
            <span>Sécurisé</span>
            <span>Moderne</span>
        </div>
    </div>
</div>
        </div>
    </section>
<section id="architecture">
    <div class="container">
        <h2 class="section-title fade-up" data-aos="fade-up">EXPERTISE CYBER SÉCURITÉ</h2>
        <div class="arch-grid">
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="100">
                <div class="arch-icon"><i class="fas fa-shield"></i></div>
                <h4>Sécurité Préventive</h4>
                <p>Méthodologies de prévention des cyberattaques, analyse des vecteurs de menace, durcissement des systèmes et zero trust architecture</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">Zero Trust</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">Threat Analysis</span>
                </div>
            </div>
            
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="200">
                <div class="arch-icon"><i class="fas fa-eye"></i></div>
                <h4>Monitoring Avancé</h4>
                <p>Surveillance en temps réel des infrastructures, détection d'anomalies comportementales, corrélation d'événements et alerting intelligent</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">SIEM</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">SOC</span>
                </div>
            </div>
            
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="300">
                <div class="arch-icon"><i class="fas fa-chart-line"></i></div>
                <h4>Data Monitoring</h4>
                <p>Analyse des flux de données en continu, détection des patterns suspects, monitoring des bases de données et protection des données sensibles</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">DLP</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">Data Audit</span>
                </div>
            </div>
            
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="400">
                <div class="arch-icon"><i class="fas fa-brain"></i></div>
                <h4>Logique Préventive</h4>
                <p>Développement de modèles prédictifs pour anticiper les menaces, analyse comportementale des utilisateurs et des systèmes (UEBA)</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">UEBA</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">ML</span>
                </div>
            </div>
            
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="500">
                <div class="arch-icon"><i class="fas fa-book"></i></div>
                <h4>Méthodologies Théoriques</h4>
                <p>Frameworks de cybersécurité (NIST, ISO27001), modélisation des menaces (STRIDE), analyses de risques quantitatives et qualitatives</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">NIST</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">ISO27001</span>
                </div>
            </div>
            
            <div class="arch-card fade-up" data-aos="zoom-in" data-aos-delay="600">
                <div class="arch-icon"><i class="fas fa-gears"></i></div>
                <h4>Pratiques Opérationnelles</h4>
                <p>Implémentation de solutions de détection et réponse (EDR/XDR), gestion des incidents, forensique et remédiation post-attaque</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">EDR</span>
                    <span style="background: rgba(0,255,157,0.1); border:1px solid var(--primary); padding:0.2rem 0.5rem; font-size:0.7rem;">Forensics</span>
                </div>
            </div>
        </div>
        <div style="margin-top: 4rem; text-align: center;" data-aos="fade-up">
            <div style="display: inline-block; background: rgba(0,255,157,0.05); border: 1px solid var(--primary); padding: 1rem 2rem;">
                <i class="fas fa-shield" style="color: var(--primary); margin-right: 1rem;"></i>
                <span>Expertise en prévention et monitoring cyber • Logique théorique et pratiques opérationnelles</span>
            </div>
        </div>
    </div>
</section>

    <section id="contact">
        <div class="container">
            <div class="contact-container fade-up" data-aos="flip-up" data-aos-delay="200">
                <h2 class="section-title" style="margin-bottom: 2rem;">CONTACT</h2>
                <div class="contact-email">studio@r00ting.xyz</div>
                <div class="contact-social">
                    <a href="#"><i class="fab fa-github"></i></a>
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                    <a href="#"><i class="fab fa-python"></i></a>
                    <a href="#"><i class="fab fa-java"></i></a>
                </div>
            </div>
        </div>
    </section>

<footer>
    <p>Fait avec ☕ et 🎧 en écoutant du lofi</p>
    <p style="font-size:0.8rem;">Dernière mise à jour : 3 heures du mat'</p>
</footer>

    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100,
            easing: 'ease-in-out'
        });

        const canvas = document.getElementById("grid");
        const ctx = canvas.getContext("2d");
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        let mouse = { x: -9999, y: -9999 };
        const squareSize = 80;
        const grid = [];

        function initGrid() {
            grid.length = 0;
            for (let x = 0; x < width; x += squareSize) {
                for (let y = 0; y < height; y += squareSize) {
                    grid.push({
                        x, y,
                        alpha: 0,
                        fading: false,
                        lastTouched: 0,
                    });
                }
            }
        }

        function getCellAt(x, y) {
            return grid.find(cell =>
                x >= cell.x && x < cell.x + squareSize &&
                y >= cell.y && y < cell.y + squareSize
            );
        }

        window.addEventListener("resize", () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            initGrid();
        });

        window.addEventListener("mousemove", (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;

            const cell = getCellAt(mouse.x, mouse.y);
            if (cell && cell.alpha === 0) {
                cell.alpha = 1;
                cell.lastTouched = Date.now();
                cell.fading = false;
            }
        });

        function drawGrid() {
            ctx.clearRect(0, 0, width, height);
            const now = Date.now();

            for (let i = 0; i < grid.length; i++) {
                const cell = grid[i];

                if (cell.alpha > 0 && !cell.fading && now - cell.lastTouched > 500) {
                    cell.fading = true;
                }

                if (cell.fading) {
                    cell.alpha -= 0.02;
                    if (cell.alpha <= 0) {
                        cell.alpha = 0;
                        cell.fading = false;
                    }
                }

                if (cell.alpha > 0) {
                    const centerX = cell.x + squareSize / 2;
                    const centerY = cell.y + squareSize / 2;

                    const gradient = ctx.createRadialGradient(
                        centerX, centerY, 5,
                        centerX, centerY, squareSize
                    );
                    
                    gradient.addColorStop(0, `rgba(0, 255, 157, ${cell.alpha})`);
                    gradient.addColorStop(1, `rgba(0, 0, 0, 0)`);

                    ctx.strokeStyle = gradient;
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(cell.x + 0.5, cell.y + 0.5, squareSize - 1, squareSize - 1);
                }
            }

            requestAnimationFrame(drawGrid);
        }

        initGrid();
        drawGrid();
        const fadeElements = document.querySelectorAll('.fade-up');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(el => observer.observe(el));
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        const skillCards = document.querySelectorAll('.skill-card');
        const skillObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const card = entry.target;
                    const levelBar = card.querySelector('.skill-level-bar');
                    const level = card.getAttribute('data-level');
                    if (levelBar && level) {
                        levelBar.style.width = level + '%';
                    }
                }
            });
        }, { threshold: 0.5 });

        skillCards.forEach(card => skillObserver.observe(card));
    </script>
</body>
</html>
'''

@app.route('/')
@limiter.limit("30 per minute")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TEZERE - Portfolio Développeur & Architecte")
    print("="*50)
    print("   ➜ http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)

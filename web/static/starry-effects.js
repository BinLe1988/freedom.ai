/**
 * Freedom.AI - 星空动态效果
 * Starry Night Dynamic Effects
 */

class StarryNightEffects {
    constructor() {
        this.particles = [];
        this.shootingStars = [];
        this.init();
    }

    init() {
        this.createParticlesContainer();
        this.generateParticles();
        this.generateShootingStars();
        this.addEventListeners();
        this.startAnimation();
    }

    createParticlesContainer() {
        // 创建粒子容器
        const container = document.createElement('div');
        container.className = 'particles-container';
        container.id = 'particles-container';
        document.body.appendChild(container);
    }

    generateParticles() {
        const container = document.getElementById('particles-container');
        const particleCount = 100;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // 随机位置
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight;
            
            // 随机大小
            const size = Math.random() * 3 + 1;
            
            // 随机透明度
            const opacity = Math.random() * 0.8 + 0.2;
            
            // 随机动画延迟
            const delay = Math.random() * 4;
            
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.opacity = opacity;
            particle.style.animationDelay = delay + 's';
            
            container.appendChild(particle);
            this.particles.push({
                element: particle,
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: size,
                opacity: opacity
            });
        }
    }

    generateShootingStars() {
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% 概率生成流星
                this.createShootingStar();
            }
        }, 2000);
    }

    createShootingStar() {
        const container = document.getElementById('particles-container');
        const shootingStar = document.createElement('div');
        
        shootingStar.style.position = 'absolute';
        shootingStar.style.width = '2px';
        shootingStar.style.height = '2px';
        shootingStar.style.background = 'linear-gradient(45deg, #fff, #74b9ff)';
        shootingStar.style.borderRadius = '50%';
        shootingStar.style.boxShadow = '0 0 10px #74b9ff, 0 0 20px #74b9ff, 0 0 30px #74b9ff';
        
        // 随机起始位置（屏幕边缘）
        const startX = Math.random() * window.innerWidth;
        const startY = -10;
        const endX = startX + (Math.random() - 0.5) * 400;
        const endY = window.innerHeight + 10;
        
        shootingStar.style.left = startX + 'px';
        shootingStar.style.top = startY + 'px';
        
        container.appendChild(shootingStar);
        
        // 动画流星
        const duration = 1000 + Math.random() * 2000;
        shootingStar.animate([
            {
                left: startX + 'px',
                top: startY + 'px',
                opacity: 0
            },
            {
                left: (startX + endX) / 2 + 'px',
                top: (startY + endY) / 2 + 'px',
                opacity: 1
            },
            {
                left: endX + 'px',
                top: endY + 'px',
                opacity: 0
            }
        ], {
            duration: duration,
            easing: 'ease-out'
        }).onfinish = () => {
            container.removeChild(shootingStar);
        };
    }

    addEventListeners() {
        // 鼠标移动效果
        document.addEventListener('mousemove', (e) => {
            this.createMouseTrail(e.clientX, e.clientY);
        });

        // 窗口大小改变时重新生成粒子
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // 页面滚动视差效果
        window.addEventListener('scroll', () => {
            this.handleScroll();
        });
    }

    createMouseTrail(x, y) {
        const container = document.getElementById('particles-container');
        const trail = document.createElement('div');
        
        trail.style.position = 'absolute';
        trail.style.left = x + 'px';
        trail.style.top = y + 'px';
        trail.style.width = '4px';
        trail.style.height = '4px';
        trail.style.background = 'radial-gradient(circle, #6c5ce7, transparent)';
        trail.style.borderRadius = '50%';
        trail.style.pointerEvents = 'none';
        trail.style.zIndex = '1000';
        
        container.appendChild(trail);
        
        // 淡出动画
        trail.animate([
            { opacity: 0.8, transform: 'scale(1)' },
            { opacity: 0, transform: 'scale(0)' }
        ], {
            duration: 800,
            easing: 'ease-out'
        }).onfinish = () => {
            if (container.contains(trail)) {
                container.removeChild(trail);
            }
        };
    }

    handleResize() {
        // 清除现有粒子
        const container = document.getElementById('particles-container');
        container.innerHTML = '';
        this.particles = [];
        
        // 重新生成粒子
        this.generateParticles();
    }

    handleScroll() {
        const scrollY = window.scrollY;
        const particles = document.querySelectorAll('.particle');
        
        particles.forEach((particle, index) => {
            const speed = (index % 3 + 1) * 0.1;
            particle.style.transform = `translateY(${scrollY * speed}px)`;
        });
    }

    startAnimation() {
        const animateParticles = () => {
            this.particles.forEach(particle => {
                // 更新位置
                particle.x += particle.vx;
                particle.y += particle.vy;
                
                // 边界检查
                if (particle.x < 0 || particle.x > window.innerWidth) {
                    particle.vx *= -1;
                }
                if (particle.y < 0 || particle.y > window.innerHeight) {
                    particle.vy *= -1;
                }
                
                // 应用位置
                particle.element.style.left = particle.x + 'px';
                particle.element.style.top = particle.y + 'px';
            });
            
            requestAnimationFrame(animateParticles);
        };
        
        animateParticles();
    }

    // 添加特殊效果
    addGlowEffect(element) {
        element.classList.add('glow-effect');
        setTimeout(() => {
            element.classList.remove('glow-effect');
        }, 2000);
    }

    addFloatAnimation(element) {
        element.classList.add('float-animation');
    }

    // 创建星云效果
    createNebula(x, y) {
        const container = document.getElementById('particles-container');
        const nebula = document.createElement('div');
        
        nebula.style.position = 'absolute';
        nebula.style.left = (x - 50) + 'px';
        nebula.style.top = (y - 50) + 'px';
        nebula.style.width = '100px';
        nebula.style.height = '100px';
        nebula.style.background = 'radial-gradient(circle, rgba(108, 92, 231, 0.3), transparent)';
        nebula.style.borderRadius = '50%';
        nebula.style.pointerEvents = 'none';
        nebula.style.zIndex = '999';
        
        container.appendChild(nebula);
        
        nebula.animate([
            { opacity: 0, transform: 'scale(0)' },
            { opacity: 0.6, transform: 'scale(1)' },
            { opacity: 0, transform: 'scale(1.5)' }
        ], {
            duration: 2000,
            easing: 'ease-out'
        }).onfinish = () => {
            if (container.contains(nebula)) {
                container.removeChild(nebula);
            }
        };
    }
}

// 页面加载完成后初始化效果
document.addEventListener('DOMContentLoaded', () => {
    const starryEffects = new StarryNightEffects();
    
    // 为按钮添加特殊效果
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            starryEffects.addGlowEffect(btn);
        });
        
        btn.addEventListener('click', (e) => {
            starryEffects.createNebula(e.clientX, e.clientY);
        });
    });
    
    // 为卡片添加浮动动画
    document.querySelectorAll('.card').forEach(card => {
        starryEffects.addFloatAnimation(card);
    });
    
    // 添加页面切换动画
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    document.querySelectorAll('.card, .stat-card').forEach(el => {
        observer.observe(el);
    });
});

// 导出类以供其他脚本使用
window.StarryNightEffects = StarryNightEffects;

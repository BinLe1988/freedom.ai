/**
 * Freedom.AI - 主题配置
 * Theme Configuration
 */

const ThemeConfig = {
    // 主题颜色配置
    colors: {
        primary: {
            dark: '#0a0a0f',
            secondary: '#1a1a2e',
            accent: '#6c5ce7'
        },
        gradients: {
            primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            secondary: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            accent: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            success: 'linear-gradient(135deg, #00b894 0%, #00cec9 100%)',
            warning: 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)',
            danger: 'linear-gradient(135deg, #e17055 0%, #d63031 100%)'
        },
        text: {
            light: '#ddd6fe',
            muted: '#a29bfe',
            accent: '#00cec9'
        }
    },

    // 动画配置
    animations: {
        duration: {
            fast: '0.3s',
            normal: '0.6s',
            slow: '1s'
        },
        easing: {
            smooth: 'cubic-bezier(0.4, 0, 0.2, 1)',
            bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
            elastic: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }
    },

    // 应用主题到页面
    applyTheme() {
        // 添加主题CSS类到body
        document.body.classList.add('starry-night-theme');
        
        // 动态加载主题CSS
        this.loadThemeCSS();
        
        // 初始化主题特效
        this.initThemeEffects();
        
        // 应用主题到现有元素
        this.applyThemeToElements();
    },

    // 加载主题CSS
    loadThemeCSS() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/starry-night-theme.css';
        link.id = 'starry-theme-css';
        document.head.appendChild(link);
    },

    // 初始化主题特效
    initThemeEffects() {
        // 加载星空效果脚本
        const script = document.createElement('script');
        script.src = '/static/starry-effects.js';
        script.id = 'starry-effects-js';
        document.head.appendChild(script);
    },

    // 应用主题到现有元素
    applyThemeToElements() {
        // 为导航栏添加动画
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.classList.add('slide-in-left');
        }

        // 为卡片添加动画
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });

        // 为按钮添加悬停效果
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', this.addButtonHoverEffect);
            btn.addEventListener('mouseleave', this.removeButtonHoverEffect);
        });

        // 为表单元素添加焦点效果
        const formElements = document.querySelectorAll('.form-control, .form-select');
        formElements.forEach(element => {
            element.addEventListener('focus', this.addFormFocusEffect);
            element.addEventListener('blur', this.removeFormFocusEffect);
        });
    },

    // 按钮悬停效果
    addButtonHoverEffect(e) {
        const btn = e.target;
        btn.style.transform = 'translateY(-2px) scale(1.02)';
        btn.style.boxShadow = '0 8px 25px rgba(108, 92, 231, 0.6)';
    },

    removeButtonHoverEffect(e) {
        const btn = e.target;
        btn.style.transform = 'translateY(0) scale(1)';
        btn.style.boxShadow = '0 4px 15px rgba(108, 92, 231, 0.4)';
    },

    // 表单焦点效果
    addFormFocusEffect(e) {
        const element = e.target;
        element.style.transform = 'scale(1.02)';
        element.style.boxShadow = '0 0 20px rgba(108, 92, 231, 0.4)';
    },

    removeFormFocusEffect(e) {
        const element = e.target;
        element.style.transform = 'scale(1)';
        element.style.boxShadow = 'none';
    },

    // 创建通知效果
    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification-popup`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideInFromRight 0.5s ease-out;
            backdrop-filter: blur(10px);
        `;
        
        document.body.appendChild(notification);
        
        // 自动移除
        setTimeout(() => {
            if (document.body.contains(notification)) {
                notification.style.animation = 'slideOutToRight 0.5s ease-in';
                setTimeout(() => {
                    if (document.body.contains(notification)) {
                        document.body.removeChild(notification);
                    }
                }, 500);
            }
        }, duration);
    },

    // 获取通知图标
    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            warning: 'exclamation-triangle',
            danger: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // 创建加载动画
    showLoading(container) {
        const loading = document.createElement('div');
        loading.className = 'loading-spinner';
        loading.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
        
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }
        
        if (container) {
            container.appendChild(loading);
        } else {
            document.body.appendChild(loading);
        }
        
        return loading;
    },

    // 移除加载动画
    hideLoading(loading) {
        if (loading && loading.parentElement) {
            loading.parentElement.removeChild(loading);
        }
    },

    // 创建模态框
    createModal(title, content, options = {}) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog ${options.size || ''}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // 使用Bootstrap模态框
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // 模态框关闭后移除
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
        
        return bsModal;
    },

    // 添加页面切换动画
    addPageTransition() {
        // 为所有链接添加页面切换效果
        document.querySelectorAll('a[href^="/"]').forEach(link => {
            link.addEventListener('click', (e) => {
                if (!e.ctrlKey && !e.metaKey) {
                    e.preventDefault();
                    this.transitionToPage(link.href);
                }
            });
        });
    },

    // 页面切换动画
    transitionToPage(url) {
        // 添加淡出效果
        document.body.style.opacity = '0';
        document.body.style.transform = 'scale(0.95)';
        document.body.style.transition = 'all 0.3s ease-out';
        
        setTimeout(() => {
            window.location.href = url;
        }, 300);
    },

    // 初始化主题
    init() {
        // 等待DOM加载完成
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.applyTheme();
                this.addPageTransition();
            });
        } else {
            this.applyTheme();
            this.addPageTransition();
        }
    }
};

// 自动初始化主题
ThemeConfig.init();

// 导出配置对象
window.ThemeConfig = ThemeConfig;

// 等待DOM完全加载
document.addEventListener('DOMContentLoaded', function() {
    // 获取所有模式按钮和计算部分
    const modeBtns = document.querySelectorAll('.mode-btn');
    const calcSections = document.querySelectorAll('.calc-section');
    
    // 添加模式切换功能
    modeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 移除所有按钮的active类
            modeBtns.forEach(b => b.classList.remove('active'));
            
            // 为当前点击的按钮添加active类
            this.classList.add('active');
            
            // 获取当前模式
            const mode = this.getAttribute('data-mode');
            
            // 隐藏所有计算部分
            calcSections.forEach(section => {
                section.classList.add('hidden');
            });
            
            // 显示选中的计算部分
            document.getElementById(`${mode}-section`).classList.remove('hidden');
        });
    });
    
    // 为数字输入添加增强体验
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        // 输入时添加交互效果
        input.addEventListener('input', function() {
            if (this.value) {
                this.style.borderColor = '#48dbfb';
            } else {
                this.style.borderColor = '#e0e0e0';
            }
        });
        
        // 添加键盘快捷键支持：按Enter提交表单
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.closest('form').querySelector('.calculate-btn').click();
            }
        });
    });
    
    // 高亮表单结果
    const resultContainer = document.querySelector('.result-container');
    if (resultContainer) {
        // 滚动到结果区域
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // 添加轻微闪光效果
        setTimeout(() => {
            resultContainer.style.boxShadow = '0 0 15px rgba(72, 219, 251, 0.5)';
            setTimeout(() => {
                resultContainer.style.boxShadow = 'inset 0 0 6px rgba(0, 0, 0, 0.1)';
            }, 800);
        }, 200);
    }
    
    // 为方程求解添加可视化效果
    const equationInputs = document.querySelectorAll('#equation-section input');
    const updateEquationPreview = () => {
        const a = document.getElementById('eq-a').value || '1';
        const b = document.getElementById('eq-b').value || '0';
        const c = document.getElementById('eq-c').value || '0';
        
        // 格式化系数字符串
        let eqStr = '';
        
        // 处理a系数
        if (a === '1') eqStr += 'x²';
        else if (a === '-1') eqStr += '-x²';
        else eqStr += `${a}x²`;
        
        // 处理b系数
        if (b === '0') {
            // 不显示b项
        } else if (b === '1') {
            eqStr += ' + x';
        } else if (b === '-1') {
            eqStr += ' - x';
        } else if (parseFloat(b) > 0) {
            eqStr += ` + ${b}x`;
        } else {
            eqStr += ` - ${Math.abs(parseFloat(b))}x`;
        }
        
        // 处理c系数
        if (c === '0') {
            // 不显示c项
        } else if (parseFloat(c) > 0) {
            eqStr += ` + ${c}`;
        } else {
            eqStr += ` - ${Math.abs(parseFloat(c))}`;
        }
        
        eqStr += ' = 0';
        
        // 更新方程显示
        const equationFormat = document.querySelector('.equation-format');
        if (equationFormat) {
            equationFormat.textContent = eqStr;
        }
    };
    
    // 为方程求解输入框添加监听器
    equationInputs.forEach(input => {
        input.addEventListener('input', updateEquationPreview);
    });
    
    // 初始更新方程显示
    if (document.getElementById('equation-section')) {
        updateEquationPreview();
    }
    
    // 添加一些有趣的彩蛋
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.addEventListener('click', function() {
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0)';
            }, 1000);
        });
    }
});
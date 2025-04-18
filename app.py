from flask import Flask, render_template, request
import math
import argparse

app = Flask(__name__)

# 设置应用的基本信息
app.config['TITLE'] = "PL高级计算器"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = None
    last_operation = None
    a_value = ""
    b_value = ""
    
    if request.method == "POST":
        try:
            operation = request.form.get("operation", "basic")
            
            # 基本运算
            if operation == "basic":
                a = float(request.form["a"])
                b = float(request.form["b"])
                basic_op = request.form["basic_op"]
                a_value = a
                b_value = b
                
                if basic_op == "add":
                    result = a + b
                    expression = f"{a} + {b}"
                elif basic_op == "subtract":
                    result = a - b
                    expression = f"{a} - {b}"
                elif basic_op == "multiply":
                    result = a * b
                    expression = f"{a} × {b}"
                elif basic_op == "divide":
                    if b == 0:
                        result = "错误：除数不能为零"
                        expression = f"{a} ÷ {b}"
                    else:
                        result = a / b
                        expression = f"{a} ÷ {b}"
                elif basic_op == "power":
                    result = a ** b
                    expression = f"{a}^{b}"
                elif basic_op == "root":
                    if a < 0 and b % 2 == 0:
                        result = "错误：偶次根号下不能为负数"
                    else:
                        result = a ** (1/b)
                        expression = f"{b}√{a}"
                
                last_operation = "basic"
            
            # 高级函数
            elif operation == "function":
                x = float(request.form["x"])
                func = request.form["function"]
                a_value = x
                
                if func == "sin":
                    result = math.sin(math.radians(x))
                    expression = f"sin({x}°)"
                elif func == "cos":
                    result = math.cos(math.radians(x))
                    expression = f"cos({x}°)"
                elif func == "tan":
                    if abs(math.cos(math.radians(x))) < 1e-10:
                        result = "错误：tan(90°+180n°)无意义"
                    else:
                        result = math.tan(math.radians(x))
                        expression = f"tan({x}°)"
                elif func == "log10":
                    if x <= 0:
                        result = "错误：对数的真数必须为正数"
                    else:
                        result = math.log10(x)
                        expression = f"log₁₀({x})"
                elif func == "ln":
                    if x <= 0:
                        result = "错误：对数的真数必须为正数"
                    else:
                        result = math.log(x)
                        expression = f"ln({x})"
                elif func == "sqrt":
                    if x < 0:
                        result = "错误：实数范围内平方根的真数不能为负数"
                    else:
                        result = math.sqrt(x)
                        expression = f"√{x}"
                
                last_operation = "function"

            # 方程求解
            elif operation == "equation":
                a = float(request.form["eq_a"])
                b = float(request.form["eq_b"])
                c = float(request.form["eq_c"])
                a_value = a
                b_value = b
                
                # 一元二次方程: ax² + bx + c = 0
                discriminant = b**2 - 4*a*c
                expression = f"{a}x² + {b}x + {c} = 0"
                
                if a == 0:
                    if b == 0:
                        if c == 0:
                            result = "方程无穷多解"
                        else:
                            result = "方程无解"
                    else:
                        x = -c / b
                        result = f"x = {x}"
                elif discriminant > 0:
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    result = f"x₁ = {x1:.4f}, x₂ = {x2:.4f}"
                elif discriminant == 0:
                    x = -b / (2*a)
                    result = f"x₁ = x₂ = {x:.4f}"
                else:
                    real = -b / (2*a)
                    imag = math.sqrt(abs(discriminant)) / (2*a)
                    result = f"x₁ = {real:.4f} + {imag:.4f}i, x₂ = {real:.4f} - {imag:.4f}i"
                
                last_operation = "equation"
            
            # 格式化数字结果
            if isinstance(result, float):
                # 如果接近整数，则去掉小数部分
                if abs(result - round(result)) < 1e-10:
                    result = int(round(result))
                # 限制小数位数
                else:
                    result = round(result, 6)
                    # 去掉末尾的0
                    result = str(result).rstrip('0').rstrip('.') if '.' in str(result) else result
            
        except Exception as e:
            result = f"计算错误: {str(e)}"
    
    return render_template("index.html", 
                          result=result, 
                          expression=expression, 
                          last_operation=last_operation,
                          a=a_value,
                          b=b_value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PL高级计算器')
    parser.add_argument('--port', type=int, default=5001, help='指定端口号')
    args = parser.parse_args()
    
    app.run(debug=True, port=args.port)
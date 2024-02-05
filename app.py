from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


def format_polynomial(coefficients):
    degree = len(coefficients) - 1

    def term(coef, exp):
        if int(coef) == coef:
            coef = int(coef)
        if exp == 0:
            return str(coef)
        elif exp == 1:
            return f"{coef}x"
        else:
            return f"{coef}x^{exp}"

    def superscript(exp):
        # Map each digit to its corresponding Unicode superscript character
        superscript_chars = {"0": "⁰", "1": "¹", "2": "²", "3": "³",
                             "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
        return "".join(superscript_chars[digit] for digit in str(exp))

    terms = [term(coef, exp) for exp, coef in enumerate(
        reversed(coefficients)) if coef != 0]

    if not terms:
        return "0"
    else:
        formatted_equation = " + ".join(terms[::-1])
        for exp in range(degree, 0, -1):
            formatted_equation = formatted_equation.replace(
                f"^{exp}", superscript(exp))
        return formatted_equation


def format_imaginary_part(imaginary_part):
    # Check if the imaginary part is 1 or -1
    if imaginary_part == 1:
        return "i"
    elif imaginary_part == -1:
        return "-i"

    # Check if the imaginary part is an integer
    elif imaginary_part.is_integer():
        return f"{int(imaginary_part)}i"

    # Format the imaginary part with up to 5 decimal places
    else:
        formatted_imaginary = f"{imaginary_part:.5f}"
        # Remove trailing zeros after the decimal point
        formatted_imaginary = formatted_imaginary.rstrip('0').rstrip(
            '.') if '.' in formatted_imaginary else formatted_imaginary
        return f"{formatted_imaginary}i"


def find_roots(coefficients):
    roots = np.roots(coefficients)
    real_parts = np.real(roots)
    imaginary_parts = np.imag(roots)
    ans = []
    l = len(roots)

    for i in range(l):
        if imaginary_parts[i] == 0:
            if real_parts[i].is_integer():
                ans.append(str(int(real_parts[i])))
            else:
                formatted_real = f"{real_parts[i]:.5f}"
                formatted_real = formatted_real.rstrip('0').rstrip(
                    '.') if '.' in formatted_real else formatted_real
                ans.append(formatted_real)
        elif real_parts[i] == 0:
            ans.append(format_imaginary_part(imaginary_parts[i]))
        else:
            if real_parts[i].is_integer():
                real_part_str = str(int(real_parts[i]))
            else:
                formatted_real = f"{real_parts[i]:.5f}"
                formatted_real = formatted_real.rstrip('0').rstrip(
                    '.') if '.' in formatted_real else formatted_real
                real_part_str = formatted_real

            imaginary_part_str = format_imaginary_part(imaginary_parts[i])

            ans.append(f"{real_part_str} + {imaginary_part_str}")

    goodlook = " <br><br> ".join(ans)
    return goodlook


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        coefficients_str = request.form['coefficients']
        coefficients = [float(x) for x in coefficients_str.split(',')]
        Equation = format_polynomial(coefficients)
        roots = find_roots(coefficients)
        return render_template('index.html', roots=roots, Equation=Equation)

    return render_template('index.html', roots=None, Equation=None)


if __name__ == '__main__':
    app.run(port=5000)

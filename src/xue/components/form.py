from ..core import Div, Label, Span, P, Form as CoreForm, Script, Head
from .input import input

def Form(*children, **kwargs):
    return CoreForm(*children, **kwargs)

def FormField(label, name, type="text", placeholder="", description=None, **kwargs):
    field_id = f"{name}-field"
    return Div(
        Label(label, for_=field_id, class_="block text-sm font-medium text-gray-700"),
        input(type=type, id=field_id, name=name, placeholder=placeholder, **kwargs),
        P(description, class_="mt-2 text-sm text-gray-500") if description else None,
        Span(id=f"{name}-error", class_="text-sm text-red-500 hidden"),
        class_="mb-4"
    )

# def FormButton(text, **kwargs):
#     return input(type="submit", value=text, class_="px-6 py-3 flex items-center justify-center text-lg w-full md:w-auto lg:w-48 h-12 bg-blue-500 text-white rounded hover:bg-blue-600", **kwargs)
#     # return input(type="submit", value=text, class_="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600", **kwargs)

# 添加表单验证脚本
Head.add_default_children([
    Script("""
        function validateForm(event) {
            event.preventDefault();
            let isValid = true;
            const form = event.target;
            const fields = form.querySelectorAll('input[name], select[name], textarea[name]');

            fields.forEach(field => {
                const errorSpan = document.getElementById(`${field.name}-error`);
                errorSpan.textContent = '';
                errorSpan.classList.add('hidden');

                if (field.hasAttribute('required') && !field.value) {
                    errorSpan.textContent = 'This field is required.';
                    errorSpan.classList.remove('hidden');
                    isValid = false;
                }

                if (field.type === 'email' && field.value && !/\S+@\S+\.\S+/.test(field.value)) {
                    errorSpan.textContent = 'Please enter a valid email address.';
                    errorSpan.classList.remove('hidden');
                    isValid = false;
                }
            });

            if (isValid) {
                console.log('Form is valid');
                // 在这里添加表单提交逻辑
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', validateForm);
            });
        });
    """, id="form-validation-script")
])
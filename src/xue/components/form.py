from ..core import Div, Label, Span, P, Form as CoreForm, Script, Head, Style
from .input import input

Head.add_default_children([
    Style("""
        .form-field {
            margin-bottom: 1rem;
        }
        .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: #111827;
            transition: color 0.2s ease-in-out;
        }
        .form-description {
            font-size: 0.875rem;
            color: #6b7280;
            margin-top: 0.5rem;
            transition: color 0.2s ease-in-out;
        }
        .form-error {
            font-size: 0.875rem;
            color: #ef4444;
            margin-top: 0.5rem;
            transition: color 0.2s ease-in-out;
        }
        @media (prefers-color-scheme: dark) {
            .form-label {
                color: #f3f4f6;
            }
            .form-description {
                color: #9ca3af;
            }
            .form-error {
                color: #f87171;
            }
        }
    """, id="form-style")
])

def Form(*children, **kwargs):
    return CoreForm(*children, **kwargs)

def FormField(label, name, type="text", placeholder="", description=None, **kwargs):
    field_id = f"{name}-field"
    return Div(
        Label(label, for_=field_id, class_="form-label"),
        input(type=type, id=field_id, name=name, placeholder=placeholder, **kwargs),
        P(description, class_="form-description") if description else None,
        Span(id=f"{name}-error", class_="form-error hidden"),
        class_="form-field"
    )

# 保留原有的表单验证脚本
Head.add_default_children([
    Script(r"""
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
from ..core import Div, H3, P, Form, Label, Input, Button

def Card(*children, class_="", **kwargs):
    return Div(*children, class_=f"bg-white shadow-md rounded-lg {class_}", **kwargs)

def CardHeader(*children, class_="", **kwargs):
    return Div(*children, class_=f"px-6 py-4 border-b {class_}", **kwargs)

def CardTitle(text, class_="", **kwargs):
    return H3(text, class_=f"text-xl font-semibold {class_}", **kwargs)

def CardDescription(text, class_="", **kwargs):
    return P(text, class_=f"text-sm text-gray-600 {class_}", **kwargs)

def CardContent(*children, class_="", **kwargs):
    return Div(*children, class_=f"px-6 py-4 {class_}", **kwargs)

def CardFooter(*children, class_="", **kwargs):
    return Div(*children, class_=f"px-6 py-4 border-t flex justify-between {class_}", **kwargs)

def FormField(label, input_type="text", placeholder="", id=""):
    return Div(
        Label(label, for_=id, class_="block text-sm font-medium text-gray-700"),
        Input(type=input_type, id=id, placeholder=placeholder, class_="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"),
        class_="mb-4"
    )
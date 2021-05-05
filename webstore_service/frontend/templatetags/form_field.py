from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# @register.filter("add_class")
# def add_class(value, arg):
#     value_with_class = value.split(" ", 1)[0] + f" class={arg} " + value.split(" ", 1)[1]
#     print(value_with_class, arg)
#     return value_with_class



def form_tags(parser, token):
    try:
        # unpack arguments
        _, html_tag, *html_attributes = token.split_contents()
    # if no correct number of arguments
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.split_contents()[0]} requires any HTML attributes (class, style, ...) but no one was found")
    # check correctness of arguments
    for arg in html_attributes:
        try:
            # check if html tag is no enclosed in collons
            if arg.split("=")[1][0] != arg.split("=")[1][-1] and arg.split("=")[1][0] not in ["'", '"']:
                raise template.TemplateSyntaxError('HTML tag attributes must be enclosed in ""')
        # check if class has no equal sign
        except IndexError:
            raise template.TemplateSyntaxError(f"Invalid HTML tag attribute '{arg}'")
    return form_tags_render(html_tag, html_attributes)

class form_tags_render(template.Node):
    def __init__(self, html_tag, html_attributes):
        # saves the passed obj parameter for later use
        # this is a template.Variable, because that way it can be resolved
        # against the current context in the render method
        self.__html_tag = template.Variable(html_tag)
        self.__html_attributes = html_attributes
    
    # render html tag with attributes
    def render(self, context):
        try:
            self.__form_field = str(self.__html_tag.resolve(context))
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError(f"{self.__html_tag} doesn't exist in form {context['form'].__class__.__name__}")
        # join all attributes in a single string
        self.__attrib_string = str.join(" ", self.__html_attributes)
        # print(self.__form_field)
        return self.__form_field.split(" ", 1)[0] + " " + mark_safe(self.__attrib_string) + " " + self.__form_field.split(" ", 1)[1]

register.tag("form_field", form_tags)
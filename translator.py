import argparse
import xml.etree.ElementTree as ET

def process_comment(element):
    """Обрабатывает комментарии."""
    lines = [child.text for child in element.findall("line")]
    if len(lines) == 1:
        return f"\\ {lines[0]}"
    else:
        return f"=begin\n{chr(10).join(lines)}\n=cut"

def process_constant(element):
    """Обрабатывает константы."""
    name = element.get("name")
    value_element = element.find("value")
    value_type = value_element.get("type")

    if value_type == "integer":
        expression = value_element.find("expression")
        if expression is not None:
            return process_expression(expression, name)

        array = value_element.find("array")
        if array is not None:
            items = [item.text for item in array.findall("item")]
            return f"{name} is << {', '.join(items)} >>"
        else:
            return f"{name} is {value_element.text}"

    elif value_type == "string":
        array = value_element.find("array")
        if array is not None:
            items = [f'\"{item.text}\"' for item in array.findall("item")]
            return f"{name} is << {', '.join(items)} >>"
        else:
            return f"{name} is \"{value_element.text}\""

    else:
        raise ValueError(f"Unsupported constant type: {value_type}")

def process_expression(element, name=None):
    """Обрабатывает выражения."""
    operation = element.get("operation")
    operands_element = element.find("operands")
    operands = [operand.text for operand in operands_element.findall("operand")]

    if operation == "add":
        result = f"$+ {' '.join(operands)}$"
    elif operation == "abs":
        result = f"$abs {operands[0]}$"
    else:
        raise ValueError(f"Unsupported operation: {operation}")

    if name:
        return f"{name} is {result}"
    return result

def process_xml_element(element):
    """Обрабатывает корневой элемент XML."""
    result = []

    for child in element:
        if child.tag == "comment":
            result.append(process_comment(child))

        elif child.tag == "constant":
            result.append(process_constant(child))

        elif child.tag == "expression":
            result.append(process_expression(child))

        else:
            raise ValueError(f"Unknown element: {child.tag}")

    return "\n".join(result)

def process_xml_file(input_file):
    """Обрабатывает входной XML-файл."""
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        return process_xml_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")

def main():
    """Точка входа в программу."""
    parser = argparse.ArgumentParser(description="XML to Config Language Converter")
    parser.add_argument("--input", required=True, help="Path to input XML file")
    parser.add_argument("--output", required=True, help="Path to output configuration file")
    args = parser.parse_args()

    try:
        result = process_xml_file(args.input)
        with open(args.output, "w", encoding="utf-8") as output_file:
            output_file.write(result)
        print("Conversion successful.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

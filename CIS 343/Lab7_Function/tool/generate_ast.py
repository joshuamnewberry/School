#!/usr/bin/env python3
import sys
import os

def define_ast(output_dir, base_name, types):
    # Generate the base AST class
    with open(os.path.join(output_dir, f"{base_name.lower()}.py"), "w") as f:
        f.write(f"class {base_name}:")
        f.write(f"\n    pass")

        for type in types:
            class_name, fields = type.split(":")
            class_name = class_name.strip()
            fields = [field.strip() for field in fields.split(",")]
            
            class_definition = define_type(base_name, class_name, fields)
            f.write(class_definition)

def define_type(base_name, class_name, fields):
    class_line = f"\n\nclass {class_name}({base_name}):"
    if fields:
        args = ", ".join(fields)
        init_line = "\n    def __init__(self, " + args + "):"
        body = ""
        for field in fields:
            body += "\n        self." + field + " = " + field
    else:
        init_line = "\n    def __init__(self):"
        body = "\n        pass"
    return class_line + init_line + body

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: generate_ast [output directory]")
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "Stmt", [
        "Expression : expression",
        "Print : expression",
    ])
    print("Generated expr.py")
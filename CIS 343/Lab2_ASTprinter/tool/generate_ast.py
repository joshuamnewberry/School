#!/usr/bin/env python3
import sys
import os

def define_ast(output_dir, base_name, types):
    # Generate the base AST class
    with open(os.path.join(output_dir, f"{base_name.lower()}.py"), "w") as f:
        f.write(f"class {base_name}:\n")
        


        for type in types:
            pass
        


        f.write(define_type(base_name.strip(), class_name.strip(),\
        [field.strip() for field in fields]))
        f.write("\n")

def define_type(base_name, class_name, fields):
    ret = None
    for field in fields:
        pass
    return ret

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: generate_ast [output directory]")
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Binary : left, operator, right",
        "Grouping : expression",
        "Literal : value",
        "Unary : operator, right"
    ])
import ast
import os,sys, glob

ignore_types = ["list","set","float","int","str",
                "dict","Enum","DataFrame","ndarray",
                "BaseSettings","BaseModel"]

def class_pass(tree):
    results = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.bases: 
            for base in node.bases:
                if hasattr(base,"id") and base.id not in ignore_types:
                    results.append(f"{base.id} -> {node.name}\n")

    return set(results)
def function_pass(tree):
    results = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classname = node.name
            for fn in node.body:
                if isinstance(fn,ast.FunctionDef):
                    argum = fn.args
                    if hasattr(argum, "args"):
                        for arg in argum.args:
                            print("\t\t",fn.name)
                            if hasattr(arg, "annotation") and hasattr(arg.annotation,"id"):
                                annot = f"{arg.annotation.id}"
                                print("id",classname,annot)
                                if annot not in ignore_types:
                                    results.append(f"{classname} -> {annot} [arrowhead=icurve]")
                            if hasattr(arg, "annotation") and hasattr(arg.annotation,"attr"):
                                annot = f"{arg.annotation.attr}"
                                print("attr",classname,annot)
                                if annot not in ignore_types:
                                    results.append(f"{classname} -> {annot} [arrowhead=icurve]")
                            
    return set(results)           

def dataclass_pass(tree):
    results = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classname = node.name
            for i,fn in enumerate(node.body):
                if isinstance(fn,ast.AnnAssign) and isinstance(fn.annotation,ast.Name):
                    annot = fn.annotation.id
                    if annot not in ignore_types:
                        results.append(f"{classname} -> {annot} [arrowhead=icurve]")
    return set(results)           
def fix_filename(filename):
    filename = filename.split("/")
    filename = filename[-1]
    filename = filename.replace(".py","")
    return filename

def file_subgraph(filename):
    print(filename)
    with open(filename) as fp:
        code = fp.read()
    tree = ast.parse(code)
    classes = class_pass(tree)
    functions = function_pass(tree)
    dataclass_attrs = dataclass_pass(tree)
    output = ""
    if classes or functions:
        output += f"\n\tsubgraph _{fix_filename(filename)}" + "{\n\t"
        output += "\n\t\t".join(classes)
        output += "\n\t\t".join(dataclass_attrs)
        output += "\n\t\t".join(functions)
        output += "\n\t}"
    return output

if __name__ == "__main__":
    paths=sys.argv[1:]
    files = []
    for path in paths:
        files += glob.glob(os.path.expanduser(path), recursive = True) 
    pyfiles = [f for f in files if f[-3:]==".py"]

    graph = "digraph untitled {\n"
    graph += "\n".join([file_subgraph(codefile) for codefile in pyfiles])
    graph += "\n}"
    with open("object_graph.dot","w") as fp:
        fp.write(graph)

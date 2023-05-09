from typing import Any


def to_php(source: Any, level=0, ident="\t", comments={}) -> str:
    match source:
        case dict(source):
            res = f"{ident*level}[\n"
            level += 1
            for k, v in source.items():
                if comment := comments.get(k):
                    res += f"{ident*level}#{comment}\n"
                res += f"{ident*level}'{k}' => "
                res += to_php(v, level)
            level -= 1
            res += f"{ident*level}],\n"
            return res
        case list(source):
            res = f"{ident*level}[\n"
            level += 1
            for v in source:
                res += to_php(v, level)
            level -= 1
            res += f"{ident*level}],\n"
            return res
        case str(source):
            return f"'{source}',\n"
        case int(source):
            return f"{source},\n"
    return ""

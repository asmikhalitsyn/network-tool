from typing import Optional


def search(pattern, output, group=1) -> str:
    return pattern.search(output).group(group)


def opt_search(pattern, output, group=1) -> Optional[str]:
    try:
        return search(pattern, output, group=group)
    except AttributeError:
        return


class ImageNameSet(set[str]):

    def force_add(self, path: str) -> str:
        parts = path.split('.')
        base = parts[0]
        suffix = 1

        if len(parts) == 1:
            ext = ''
        else:
            ext = '.' + parts[1]

        while path in self:
            path = f"{base}_{suffix}{ext}"
            suffix += 1

        super().add(path)

        return path

import re, unicodedata


def norm(value):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", value or "").casefold())


def match_product(target: dict, candidate: dict) -> str:
    """Stable identifiers are necessary; variant conflicts always veto a match."""
    for field in ("manufacturer", "scale", "edition", "reissue_no"):
        a, b = target.get(field), candidate.get(field)
        if a is not None and b is not None and norm(str(a)) != norm(str(b)):
            return "REJECTED"
    if candidate.get("is_set"):
        return "REJECTED"
    for field in ("jan_code", "sku"):
        if target.get(field) and candidate.get(field):
            if norm(target[field]) != norm(candidate[field]):
                return "REJECTED"
            if field == "sku" and norm(target.get("manufacturer")) != norm(
                candidate.get("manufacturer")
            ):
                continue
            # A page spanning multiple reissues is not a verified edition identifier.
            if target.get("edition") and not candidate.get("edition"):
                continue
            return "MATCHED"
    return "MATCH_REVIEW_REQUIRED"

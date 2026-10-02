import httpx

from .config import settings

SYSTEM_PROMPT = """Sen BRB bankining virtual yordamchisisan.

Qoidalar:
- Foydalanuvchi qaysi tilda yozgan bo'lsa, o'sha tilda javob ber.
- Qisqa, aniq va xushmuomala javob ber.
- Aniq bilmagan ma'lumotingni hech qachon o'ylab topma.
  Bilmasang: "Bu savolga aniq javob bera olmayman" deb ayt.
"""


def chat(messages: list[dict]) -> str:
    payload = {
        "model": settings.model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.1,
    }

    response = httpx.post(
        f"{settings.base_url}/chat/completions",
        json=payload,
        timeout=settings.timeout,
    )

    response.raise_for_status()
    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    return answer


def main() -> None:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("BRB AI yordamchisi.Chiqish uchun 'exit' bosing ")

    while True:
        try:
            savol = input("\n Siz: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nXayr!")
            break
        if not savol:
            continue
        if savol.lower() in {"exit", "quit", "chiqish"}:
            print("Xayr!")
            break
        messages.append({"role": "user", "content": savol})

        try:
            javob = chat(messages)
        except httpx.HTTPError as e:
            print(f"XATOLIK : {e}")
            messages.pop()
            continue
        messages.append({"role": "assistant", "content": javob})
        print(f"BRB AI: {javob}")


if __name__ == "__main__":
    main()

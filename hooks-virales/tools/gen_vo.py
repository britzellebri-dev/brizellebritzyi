"""Voz en off: edge-tts es-DO-RamonaNeural -> assets/vo/<id>.mp3 + tools/words.json (tiempos por palabra)."""
import asyncio, json, os, edge_tts
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
VOICE, RATE = "es-DO-RamonaNeural", "+12%"
async def one(L):
    c = edge_tts.Communicate(L.get("say", L["text"]), VOICE, rate=L.get("rate", RATE), boundary="WordBoundary")
    audio, words = bytearray(), []
    async for m in c.stream():
        if m["type"] == "audio": audio += m["data"]
        elif m["type"] == "WordBoundary":
            words.append({"w": m["text"], "s": m["offset"] / 1e7, "e": (m["offset"] + m["duration"]) / 1e7})
    open(os.path.join(ROOT, "assets/vo", L["id"] + ".mp3"), "wb").write(audio)
    return L["id"], words
async def main():
    lines = json.load(open(os.path.join(HERE, "lines.json")))
    out = {}
    for L in lines:
        k, w = await one(L); out[k] = w
    json.dump(out, open(os.path.join(HERE, "words.json"), "w"), ensure_ascii=False, indent=1)
asyncio.run(main())

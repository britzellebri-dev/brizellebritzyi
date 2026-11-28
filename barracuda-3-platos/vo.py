import asyncio,json,edge_tts,subprocess,sys
V=sys.argv[1] if len(sys.argv)>1 else 'es-PR-VictorNeural'
L=json.load(open('lines.json')); words={}
async def one(k,t):
    c=edge_tts.Communicate(t,V,rate='+10%',boundary='WordBoundary'); ws=[]
    with open(f'vo/{k}.mp3','wb') as f:
        async for ch in c.stream():
            if ch['type']=='audio': f.write(ch['data'])
            elif ch['type']=='WordBoundary': ws.append([ch['offset']/1e7,(ch['offset']+ch['duration'])/1e7,ch['text']])
    words[k]=ws
async def main(): await asyncio.gather(*[one(k,t) for k,t in L.items()])
asyncio.run(main())
dur={}
for k in L:
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'vo/{k}.mp3','-ar','48000','-ac','1',f'vo/{k}.wav'])
    dur[k]=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'vo/{k}.wav']))
json.dump(words,open('vo/words.json','w'),ensure_ascii=False,indent=0); json.dump(dur,open('vo/dur.json','w'),indent=0)
print(dur); print(words['p2b'])

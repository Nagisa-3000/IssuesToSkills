import pathlib,json,subprocess,urllib.request,hashlib,tarfile,time,os
p=pathlib.Path('/home/chenyujia/tritonToLlvm/arex-skill-graph')
d=p/'tmp/historical-python37-runtime-preparation-v1-20261006'
d.mkdir(exist_ok=False)
url='https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tar.xz'
start=time.monotonic()
with urllib.request.urlopen(url,timeout=120) as response:
 data=response.read(40*1024**2+1)
assert len(data)<=40*1024**2
archive=d/'Python-3.7.17.tar.xz';archive.write_bytes(data)
source=d/'source';source.mkdir()
with tarfile.open(archive) as stream:stream.extractall(source,filter='data')
work=source/'Python-3.7.17'
prefix=d/'python-root'
assert prefix.resolve().is_relative_to(p.resolve())
env={key:value for key,value in os.environ.items() if key in {'PATH','HOME','USER','LOGNAME','SHELL','LANG','LC_ALL','TMPDIR'}}
rows=[]
for name,argv in [('configure',['./configure','--prefix='+str(prefix),'--without-ensurepip']),('build',['make','-j2']),('install',['make','install'])]:
 with (d/(name+'.log')).open('w') as log:
  result=subprocess.run(argv,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
 row={'phase':name,'exit_code':result.returncode};rows.append(row)
 (d/'progress.json').write_text(json.dumps({'completed_phases':rows,'elapsed_seconds':time.monotonic()-start,'actual_LLM_calls':0},indent=2))
 if result.returncode:break
version=None
if all(row['exit_code']==0 for row in rows) and len(rows)==3:
 result=subprocess.run([str(prefix/'bin/python3.7'),'--version'],env=env,capture_output=True,text=True)
 version=(result.stdout+result.stderr).strip()
out={'schema':'historical-python37-compatibility-runtime-build-v1','source_url':url,'source_sha256_measured':hashlib.sha256(data).hexdigest(),'download_authentication':'publisher HTTPS; measured hash, not independently authenticated historical checksum','prefix':str(prefix),'phases':rows,'python_version':version,'elapsed_seconds':time.monotonic()-start,'execution_runtime_is_not_backdated':True,'runtime_is_not_claimed_available_at_original_query_time':True,'actual_LLM_calls':0,'formal_SWE_runs':0}
(d/'completion.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out),flush=True)

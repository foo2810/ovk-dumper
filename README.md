# ovk-dumper

## What's ovk-dumper
<p>
  SiglusEngineで使用されているOVKアーカイブからogg等のデータを取り出して、ファイルとして保存できます。
  今のところ3系のPythonでコンソールツールとして動きますが、気が向けばGUI版も作るかもしれません。
</p>

## Caution!
<p>
  思いつきで作っているので、色んな意味で不十分なところが多々あります。
</p>

## Usage
```
python3 ovkdump.py -s <save_dir> [-f <file> -d <dir>]
```
<pre>
  基本的に次のような感じでファイル等を指定する。オプションの位置は前後してもおｋ。
  -sオプションで保存先を指定
  -fオプションでoggファイルを指定
  -dオプションでoggファイルが格納されているディレクトリを指定
</pre>
<pre>
  次のような表記も可。
</pre>
```
python3 ovkdump.py -s save_dir -d dir1 dir2 -f file1 file2 -d dir3 -f file3
```

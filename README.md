# ovk-dumper

## What's ovk-dumper
<p>
  SiglusEngineで使用されているOVKアーカイブからogg等のデータを取り出して、ファイルとして保存できます。
  今のところ3系のPythonでコンソールツールとして動きますが、気が向けばGUI版も作るかもしれません。
</p>

## Caution!
<p>
  思いつきで作っているので、色んな意味で不十分なところが多々あります。
  また、oggファイルの抽出を目的で作ったので、その他の種類のファイルが入っていても、出力の拡張子が問答無用でoggになりますが、
  出力後に拡張子を書き換えればおそらく無問題。
</p>

## Usage
**実行**
```
python3 ovkdump.py -s <save_dir> [-f <file> -d <dir>]
```
  基本的に次のような感じでファイル等を指定する。オプションの位置は前後してもおｋ。
  -dオプションを使えば、ovkファイルをまとめて処理できます。<br>
  -sオプションで保存先を指定<br>
  -fオプションでovkファイルを指定<br>
  -dオプションでovkファイルが格納されているディレクトリを指定<br>
  
<pre>
  次のような表記も可。
</pre>
```
python3 ovkdump.py -s save_dir -d dir1 dir2 -f file1 file2 -d dir3 -f file3
```

**出力**
<p>
  ovkファイルごとにディレクトリで分けてファイル出力します。また、ファイル名は[ovkのファイル名]_[数字].oggとなります。
  数字はovk内の格納順で決まります。
</p>


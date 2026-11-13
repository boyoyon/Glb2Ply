<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <h1><center>Glb2Ply</center></h1>
        <h2>なにものか？</h2>
        <p>
          ・Depth Anything v3 の WEBデモなど, RGB画像から奥行き推定や3D化をした結果は glbでしかダウンロードできない。<br>
          ・glb の点群に RGB情報が見当たらなかったため, 点群に元のRGB画像の色情報を付加してみた。<br>
          　(多分探せば良いツールがいくらでもありそうだけど･･･)<br>
          ・glb/glTF の仕様書を確認していない適当な実装。<br>
            <br>
        　いまさら････<br>
            　trimesh の vertext 毎に visual.vertex_colors で RGBA が格納されていた････ <br>
            　orz 仕様書を読んでおけば･･･<br>
         　python　src\simple_glb2ply.py　(glbファイル)<br>
            <br>
            <img src="images/glb2ply.svg">
        </p>
        <h2>環境構築方法</h2>
        <p>
            pip install opencv-python open3d trimesh
        </p>
        <h2>使い方</h2>
        <p>
           ● GLBファイルにRGB情報を付加してPLYファイルとして書き出す。<br>
            python glb2ply.py  (RGB画像ファイル)  (glbファイル)  [(zスケール)]<br>
<br>
           ● PLYファイルの確認方法<br>
            python o3d_display_ply.py (plyファイル)<br>

　　　　　　 <table border="1">
                <tr><th>操作</th><th>機能</th></tr>
                <tr><td>左ボタン押下＋ドラッグ</td><td>3Dモデルの回転</td></tr>
                <tr><td>ホイールボタン押下＋ドラッグ</td><td>3Dモデルの移動</td></tr>
                <tr><td>ホイール回転</td><td>3Dモデルの拡大・縮小</td></tr>
                <tr><td>PrintScreenキー押下</td><td>スクリーンショット保存</td></tr>
                <tr><td>ESCキー押下 または ウィンドウ閉じるボタン押下　</td><td>プログラム終了</td></tr>
            </table>
<br>
            ● 点群PLYのメッシュ化<br>
            　python o3d_pcd_to_mesh.py (plyファイル)<br>
             <br>
            ● GLBファイルにテクスチャー座標を付加してPLYファイルとして書き出す。<br>
            　python glb2ply_denseUV.py (RGB画像ファイル) (glbファイル)　[(zスケール)　(スキップ)]<br>
            　点群をドロネー分割してメッシュ化(点が多いので間引く)、テクスチャー座標付加<br>
             <br>
            ● テクスチャー座標付きplyの表示<br>
            (環境構築) pip install PyOpenGL glfw plyfile<br>
            (実行)　python RgbPly.py (RGB画像ファイル)　(テクスチャー座標付きplyファイル)<br>
<br>
            ・スキップに100を指定した場合<br>
            <img src="images/skip100.gif"><br>
            ・スキップに1000を指定した場合<br>
            <img src="images/skip1000.gif"><br>
        </p>
        <h2>備忘録</h2>
        <p>
        ・GLBファイルにはオブジェクトの点群とカメラの点群が格納されていた。<br>
        ・カメラの点群は, 16個の(x,y,z)座標。<br>
        ・カメラパラメータかと思ったが, それっぽい値(0や1)が全くなく、カメラの視錐体(ピラミッド)と想定。<br>
        ・ピラミッドの頂点なら5点で良いがなぜ16個もデータがある？<br>
        ・データを見るとユニークな座標は5種類。<br>
        　→ ピラミッドの辺は8個 <br>
        　→ 始点と終点で16個格納されていると想像。<br>
         <img src="images/glb2ply2.svg"><br>
         ・上図の配置を想定。<br>
         ・z 座標が一番大きい点を p<sub>0</sub> としてオブジェクトの各点と p<sub>0</sub> を結ぶ直線と
面 p<sub>1</sub>p<sub>2</sub>p<sub>4</sub>p<sub>3</sub> の交点の座標のRGB画像の色を点群に付加した。<br>
<br>
         ・MVS(多視点ステレオ)の場合は複数のカメラが異なる方向を向くので, p<sub>0</sub> と ワールド座標の z 軸方向が一致しなくなる。<br>
         python src\glb2ply_noRGB.py data\mvs.glb<br>
         <br>
         <img src="images/mvs.svg"><br>
       　まじめに p<sub>0</sub> を抽出をしないといけない。(同一平面にある p<sub>1</sub>p<sub>2</sub>p<sub>3</sub>p<sub>4</sub> と p<sub>0</sub> を判別する)<br>
         (例) src/find_outlier_point.py
</p>
<h2>Click3R (やりたかった事はできたみたいだけど、いまいち･･･)</h2>
<p>
人のアシスト(対応点を数点クリックする)ありのMVS(Multi-View Stereo)の模様
</p>

<p>
(paper) <a href="https://arxiv.org/abs/2611.12875">https://arxiv.org/abs/2611.12875</a><br>
(github) <a href="https://github.com/UVA-Computer-Vision-Lab/click3r">https://github.com/UVA-Computer-Vision-Lab/click3r</a><br>
(on-line demo) <a href="https://huggingface.co/spaces/uva-cv-lab/Click3R">https://huggingface.co/spaces/uva-cv-lab/Click3R</a>
</p>

</p>
<img src="images/click3r_on_line_demo.svg">

<p>
on-line demo の出力も glb だった<br>
またまた、仕様を確認せず、データからテキトーに点群 PLY を作成してみる。
</p>

<p>
[1] Click3R の on-line demo で出来た glb をPLYに変換する<br>
　・python　click3r\src\click3rglb2ply.py　 (on-line demoでできたglbファイル)
<br><br>
　　geometry_*.ply ができる。<br>
<br>
　　geometry_0: 点群<br>
　　geometry_1~: メッシュ<br>
　　・geometry_1：カメラ１の投影面？vertices:4x3, faces:4x3<br>
　　・geometry_2：カメラ１の視錐体？vertices:14x3, faces:48x3<br>
　　・geometry_3：カメラ２の投影面？vertices:4x3, faces:4x3<br>
　　・geometry_4：カメラ２の視錐体？vertices:14x3, faces:48x3<br>
　　・geometry_5～：？？？
</p>

<p>
[2] できたPLY を全部表示してみる<br>
　・python　click3r\src\o3d_display_plys.py　geometry*.ply<br>
</p>
<img src="click3r/images/point_cloud_and_meshes.svg">
<p>
　位置関係がわかるように座標軸も表示する<br>
　・python　src_  click3r\src\o3d_display_ply2.py<br>
　　geometry_0.ply　geometry_1.ply　geometry_2.ply<br>
　　geometry_3.ply　geometry_4.ply　click3r\data\axisXYZ.ply<br>
<br>
　※ 色情報の無い点群はOpen3D Visualizerが色を付ける<br>
　　　1押下：z値(デフォルト)、2押下：x値、3押下：y値、･･･ 
</p>

<img src="click3r/images/point_cloud_cameras.png">

<p>
　投影面：geometry_1,　geometry_3<br>
<br>
　　vertices:　頂点の4点<br>
　　faces： 三角形分割した2枚×(裏表：2)＝4枚
</p>

<img src="click3r/images/frame.svg">

<p>
　視錐体：geometry_2,　geometry_4<br>
<br>
　　vertices:　ピラミッドの頂点(5点)＋表示用に太らせるための点(9点)と憶測･･･<br>
　　最初の5点の内、同一平面内にない点をカメラ中心と想定<br>
</p>

<img src="click3r/images/pyramid.svg">

<p>
　・投影面の頂点は geometry_1,　geometry_3 から取得<br>
　・カメラ中心は geometry_2,　geometry_4 から取得<br>
　・点群内の点と、カメラ中心を結ぶ直線が投影面と交わる点を求め<br>
　　その座標のマスクが閾値以上なら、画像の色を点群内の点に割り当てる<br>
　　処理を複数のカメラで実施する<br>
</p>

<img src="click3r/images/get_color.svg">

<p>
　[3] GLB→PLY<br>
<br>
　引数が多いので、config ファイルを指定することにした。<br>
　python　click3r\src\glb2ply.py　(configファイル)<br>
<br>
　～configファイル～<br>
<br>
　　[PLYS]<br>
　　point_cloud:　(geometry_0 を格納したPLYファイル)<br>
<br>
　　frame1:　(geometry_1 を格納したPLYファイル)<br>
　　pyramid1:　(geometry_2 を格納したPLYファイル)<br>
<br>
　　frame2:　(geometry_3 を格納したPLYファイル)<br>
　　pyramid2:　(geometry_4 を格納したPLYファイル)<br>
<br>
　　[IMAGES]<br>
　　image1:　(画像1)<br>
　　image1_mask:　(画像1のマスク)<br>
<br>
　　image2: 　(画像2)<br>
　　image2_mask:　(画像2のマスク)<br>
<br>
　～変換したPLYの表示例～<br>
　　　いまいち･･･
</p>

<img src="click3r/images/result.gif">

</body>
</html>

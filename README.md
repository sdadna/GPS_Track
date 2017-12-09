# baiduMap
**百度地图API使用　2015年末 总结整理**

1.添加覆盖物，以及给覆盖物添加点击事件。

说明文章：http://blog.csdn.net/liusaint1992/article/details/50070839

演示地址：http://runningls.com/demos/baidumap/index.html?to=marker

2.自定义的方法来根据坐标点计算地图合适的中心坐标和缩放级别。（后来知道百度有实现这个功能的API。。。）

说明文章：http://blog.csdn.net/liusaint1992/article/details/50071613

演示地址：http://runningls.com/demos/baidumap/index.html?to=zoom

3.实时轨迹。使用随机生成的坐标。不断更新轨迹。并且在轨迹生长的过程中自动调整地图的显示范围。

说明文章：http://blog.csdn.net/liusaint1992/article/details/50072929

演示地址：http://runningls.com/demos/baidumap/index.html?to=track

4.轨迹回放。选择某个时间段，根据轨迹点的顺序和时间显示轨迹。

说明文章：http://blog.csdn.net/liusaint1992/article/details/50082781

演示地址：http://runningls.com/demos/baidumap/index.html?to=trackback

5.大批量多次坐标转换结果返回顺序问题。使用闭包，解决百度坐标转换返回顺序与请求顺序不一致引起的问题。(2016.6.29)

说明文章：http://blog.csdn.net/liusaint1992/article/details/51790777

演示地址：http://runningls.com/demos/baidumap/index.html?to=translate

# modify desciption
draw line by data using baidu map API

## using file
* DrawTrack.py(trans data to track.html)
* track.html(receive data, and display it using line)
* track.ico
* socket.c(compile this file to binary,, use it to trans data to drawTrack.py)

# example
1. step1
> python DrawTrack.py
2. step2
> input [127.0.0.1:8000](http://127.0.0.1:8000) in the web
3. step3
> ./a.out

## Attention
- **The lantitude and longtitude just be allowed in china by using Baidu**.If you want to try other country, try it.

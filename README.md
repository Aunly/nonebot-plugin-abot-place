<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="docs/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="docs/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-abot-place

_✨ 移植于 ABot 的画板插件，可以和所有的 bot 用户一起画画！ ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Aunly/nonebot-plugin-abot-place.svg" alt="license">
</a>

<a href="https://pypi.python.org/pypi/nonebot-plugin-abot-place">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/nonebot-plugin-abot-place">
</a>

<a href="https://pypi.python.org/pypi/nonebot-plugin-abot-place">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-abot-place.svg" alt="pypi">
</a>

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

<a href="https://pdm.fming.dev">
    <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>

<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>

<a href="https://onebot.dev/">
  <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot">
</a>
<a href="https://onebot.dev/">
  <img src="https://img.shields.io/badge/OneBot-v12-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot">
</a>

<a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
  <img src="https://img.shields.io/badge/QQ%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat Group">
</a>
<a href="https://jq.qq.com/?_wv=1027&k=7LWx6q4J">
  <img src="https://img.shields.io/badge/QQ%E7%BE%A4-720053992-orange?style=flat-square" alt="QQ Chat Group">
</a>

</div>

## 📖 介绍

源于 ABot 的画板插件

![image](https://user-images.githubusercontent.com/59153990/235223489-c5dfa522-adaf-4e1e-af40-45e68733a4e2.png)

> 图片来自 https://web.archive.org/web/20170417154453/https://redditblog.com/2017/04/13/how-we-built-rplace/

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-abot-place

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-abot-place
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-abot-place
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-abot-place
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-abot-place
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_abot_place"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置, 配置均为**非必须项**

| 配置项 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| place_view_aliases | set[str] | None | "查看画板"的命令别名 |
| color_view_aliases | set[str] | None | "查看色板"的命令别名 |
| place_draw_aliases | set[str] | None | "画板作画"的命令别名 |

## 🎉 使用

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 参数 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|:----:|
| 查看画板 | 所有人 | 否 | 无限制 | chunk_x chunk_y                       | 查询指定区块的图像 |
| 查看色板 | 所有人 | 否 | 无限制 | None                                  | 查看颜色与其对应的编号 |
| 画板作画 | 所有人 | 否 | 无限制 | chunk_x chunk_y block_x block_y color | 在指定位置绘制指定颜色 |

注:

chunk_x chunk_y 为画板区块，取值为 0-31
block_x block_y 为画板区块，取值为 0-31
color 为颜色，取值为 0-255

## 🙏 感谢

在此感谢以下开发者(项目)对本项目做出的贡献：

- [ABot-Graia](https://github.com/djkcyl/ABot-Graia) 永远怀念最好的 ABot 🙏
- [nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template): 项目的 README 模板

## ⏳ Star 趋势

[![Stargazers over time](https://starchart.cc/Aunly/nonebot-plugin-abot-place.svg)](https://starchart.cc/Aunly/nonebot-plugin-abot-place)

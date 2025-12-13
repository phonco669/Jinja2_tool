# Jinja2 实时渲染工具

## 功能概述
- 输入 Jinja2 模板与 JSON 数据，右侧实时预览渲染结果。
- 内置可切换的色系模板（Default / Bootstrap / Material / Dark / High-Contrast）。
- 固定消息样式类名：`.msg`, `.info`, `.success`, `.warning`, `.error`, `.clear`。

## 使用指南
1. **启动服务**：
   - 方式一（推荐）：双击 `start.bat` 自动安装依赖并启动服务。
   - 方式二（命令行）：在终端运行 `.\start.bat` 或 `.\start.bat run`。
   - 启动后服务将在独立窗口运行，当前终端/批处理窗口会自动关闭，不会出现阻塞。
2. **停止服务**：
   - 方式一：双击 `stop.bat`。
   - 方式二（命令行）：在终端运行 `.\stop.bat` 或 `.\start.bat stop`。
3. 浏览器打开后，在页面顶部选择色系主题。
4. 在模板输入区编写内容，示例：
```
<div class="msg info">信息消息</div>
<div class="msg success">成功消息</div>
<div class="msg warning">警告消息</div>
<div class="msg error">错误消息</div>
<div class="msg clear">清除/普通消息</div>
```
4. 在数据输入区编写 JSON，上下文会参与 Jinja2 渲染。
5. 若模板未使用 `.msg.*` 类名，可在页头的 `Mapping` 面板中为 Info/Success/Warning/Error/Clear 分别填写需要套用主题的 **CSS 选择器**（如 `#warn-box`, `.alert`）。主题将对匹配元素及其子元素强制覆盖背景、文字颜色与边框颜色。

## 注意事项
- 主题在预览 iframe 中注入，不影响后端接口。
- 未使用 `.msg.*` 的元素不会受主题影响。
 - 使用映射时会添加 `!important` 以覆盖可能的内联样式；如仍无法覆盖，请检查是否使用了更高优先级的 `!important` 内联规则。

## 启动失败/网络代理故障排查
- 启动脚本会话中已清理 `HTTP_PROXY/HTTPS_PROXY`，避免 `InvalidProxyURL`。
- 若安装依赖失败但系统已安装 `Flask/Jinja2`，脚本会继续启动应用。
- 如需使用镜像加速，设置环境变量 `USE_MIRROR=1` 后运行 `start.bat`（使用清华镜像）。
- 手动安装命令：
  - `python -m pip install -r requirements.txt -i https://pypi.org/simple`
  - 如仍报错，检查代理设置或更换网络。

## 一键启动行为（无交互）
- 脚本将自动检测依赖并尝试从官方 PyPI 安装，失败后自动使用镜像重试。
- 安装完成后，应用在新窗口启动，批处理脚本退出，不会出现 `Y/N` 交互提示。

## 开发与维护
- 后端：`app.py`（Flask 渲染接口 `/render`）。
- 前端：`templates/index.html`（主题选择器、样式注入与渲染）。

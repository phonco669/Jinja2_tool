## 问题分析
- 当前主题仅对 `.msg.*` 类名生效，用户自定义的 Jinja2 模板未使用这些类名，且可能包含内联样式，导致主题切换无效。
- 需要让主题对“任意选择的 DOM 元素”生效，并可强制覆盖内联样式。

## 改造方案
- 在页面加入“选择器映射”配置面板，用户分别为 info/success/warning/error/clear 输入 CSS 选择器（如 `#warning-box`, `.alert`）。
- 渲染时注入两段样式：
  1) 基础主题样式（保留 `.msg.*`）
  2) 根据映射生成的选择器样式，形如：`<selector>, <selector> * { background: ... !important; color: ... !important; border-color: ... !important; }`
- 监听映射输入变化，实时重渲染；默认开启强制覆盖（使用 `!important`）。

## 具体实现
- 修改 `templates/index.html`：
  - 在 `<header>` 添加一个 `<details>` 面板（Mapping），提供五个输入框：Info/Success/Warning/Error/Clear。
  - 在脚本中新增：
    - `getSelectorMapping()`：收集并返回用户输入的选择器对象。
    - `buildMappingCSS(map, theme)`：根据映射与主题生成覆盖 CSS 字符串（带 `!important`）。
  - 更新 `render()`：拼接 `baseThemeCSS + mappingCSS` 并注入到 iframe 文档。
  - 将映射输入的 `input` 事件加入 `debounceRender()`。

## 验证
- 使用截图中的自定义块，给其根容器设置选择器（如 `div:first-child` 或 `#warning-box`），切换主题观察背景/文字/边框是否随主题实时变化。
- 验证对包含内联颜色的元素也能覆盖（通过 `!important`）。

## 文档更新
- 在 README 与说明文档中补充“选择器映射”用法与示例。
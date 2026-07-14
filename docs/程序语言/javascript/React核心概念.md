# 🧭 React 核心概念与 Hooks 笔记（完整整理）
https://chatgpt.com/g/g-p-684526c1e4388191ae14e556af21fbdc-reacthe-xin-gai-nian/c/6845198f-b224-800f-acd6-365e4754d08b
---

## 1. JSX 基础与作用

### 1.1 JSX 是什么
- JSX 是 JavaScript XML 的缩写，是 React 中的一种语法扩展。
- 用于在 JS 中编写类似 HTML 的结构，最终由 Babel 编译成 `React.createElement()`。

### 1.2 JSX 的基本语法
```jsx
const element = <h1 className="title">Hello, JSX!</h1>;
```
- 标签必须闭合。
- 使用 `{}` 插入表达式。
- 属性名使用 camelCase（如 `onClick`、`tabIndex`）。
- 使用 `className` 替代 `class`。
- 自定义组件必须以大写字母开头。

### 1.3 JSX 与 HTML 的关系
- JSX 并不是 HTML，而是 JS 表达式的语法糖。
- JSX 最终会被编译成 `React.createElement`。
- 使用 JSX 后通常不再单独写 HTML 页面结构。

### 1.4 JSX 中的样式处理方式

#### 1.4.1 className 类样式
```jsx
import './App.css';

function Button() {
  return <button className="primary">Click Me</button>;
}
```

#### 1.4.2 行内样式
```jsx
const styleObj = {
  color: 'red',
  backgroundColor: 'lightgray',
};

<button style={styleObj}>Inline Styled</button>
```

#### 1.4.3 样式优先级说明
- 行内样式 > className 样式。
- 不冲突属性自动合并，冲突属性以行内为准。

#### 1.4.4 动态样式
```jsx
const isActive = true;
<button className={isActive ? 'active' : 'inactive'}>Toggle</button>
```

#### 1.4.5 高级样式方案
- CSS Modules
- CSS-in-JS（如 styled-components、emotion）

---

## 2. 组件与数据流

### 2.1 函数组件本质
```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

### 2.2 props 和 state 的区别
| 项目 | props | state |
|------|-------|-------|
| 来源 | 父组件传入 | 内部定义 |
| 可变性 | 不可变 | 可变（通过 `setState`） |
| 控制权 | 外部 | 自组件内部 |

### 2.3 单向数据流与事件传递
```jsx
function Parent() {
  const handleClick = () => alert("Clicked");
  return <Child onClick={handleClick} />;
}

function Child({ onClick }) {
  return <button onClick={onClick}>Click Me</button>;
}
```

---

## 3. 命令式 vs 声明式

### 3.1 声明式编程
```jsx
const [count, setCount] = useState(0);
return <div>{count}</div>;
```

### 3.2 命令式对比
```js
const div = document.createElement('div');
div.textContent = count;
document.body.appendChild(div);
```

---

## 4. 生命周期与 Hook 的关系

### 4.2 Hook 对应生命周期行为
```jsx
useEffect(() => {
  console.log('组件挂载或更新');
  return () => console.log('组件卸载');
}, [dep]);
```

---

## 5. Hook 概念

### 5.3 Hook 是闭包 + 渲染绑定
```jsx
function Parent() {
  const [count, setCount] = useState(0);
  const increment = () => setCount(prev => prev + 1);
  return <Child onIncrement={increment} />;
}
```

---

## 6. 核心 Hook 一览

### useState 示例
```jsx
const [count, setCount] = useState(0);
<button onClick={() => setCount(count + 1)}>{count}</button>
```

### useEffect 示例
```jsx
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);
```

### useRef 示例
```jsx
const inputRef = useRef();
<input ref={inputRef} />
```

### useMemo 示例
```jsx
const total = useMemo(() => items.reduce((a, b) => a + b), [items]);
```

### useCallback 示例
```jsx
const memoizedFn = useCallback(() => doSomething(a), [a]);
```

---

## 7. useEffect 详解

### 清理机制示例
```jsx
useEffect(() => {
  const timer = setInterval(() => console.log('tick'), 1000);
  return () => clearInterval(timer);
}, []);
```

---

## 11. 自定义 Hook

### 示例
```js
function useTimer() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => setCount(c => c + 1), 1000);
    return () => clearInterval(timer);
  }, []);
  return count;
}
```

---

## 12. React 事件机制
```jsx
function Button() {
  function handleClick(e) {
    e.preventDefault();
    console.log('clicked');
  }

  return <a href="#" onClick={handleClick}>Click</a>;
}
```

---

## 13. 性能优化实践

### useMemo 示例
```jsx
const expensiveValue = useMemo(() => computeExpensive(a, b), [a, b]);
```

### useCallback 示例
```jsx
const memoizedHandler = useCallback(() => handleClick(), []);
```

### React.memo 示例
```jsx
const MemoizedComponent = React.memo(MyComponent);
```

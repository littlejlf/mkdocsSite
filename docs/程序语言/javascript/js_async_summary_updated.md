# 📚 JavaScript 异步处理方式全整理

## 1️⃣ 回调函数（Callback）

### 🧠 概念

- 最早期的异步处理方案
- 将函数作为参数传入异步操作，操作完成后手动调用

### 🧾 示例

```js
function getData(callback) {
  setTimeout(() => {
    callback(null, "data");
  }, 1000);
}

getData((err, result) => {
  if (err) {
    console.error(err);
  } else {
    console.log(result);
  }
});
```

### ⚠️ 问题

- 回调嵌套（回调地狱）
- 错误处理分散，不一致
- 控制流程复杂，难维护

---

## 2️⃣ Promise

### 🧠 概念

- ES6 引入，异步逻辑可以链式书写
- 本质是一个表示“将来可能完成或失败”的对象
- 状态：`pending` → `fulfilled` / `rejected`

### 🧾 示例

```js
function getData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve("data");
    }, 1000);
  });
}

getData()
  .then(result => {
    console.log(result);
  })
  .catch(error => {
    console.error(error);
  });
```

### ✅ 优点

- 链式结构更清晰
- 集中错误处理（`.catch()`）
- 支持并发（`Promise.all`, `Promise.race`）
- 多个异步的操作用多个then去连接即可，并可以用多个.catch捕获错误

---

## 3️⃣ async / await

### 🧠 概念

- ES2017 引入，是 Promise 的语法糖
- `async` 标记函数为异步函数，`await` 暂停执行直到 Promise 解析 ，只有async修饰的函数才可以使用await这个标识符

### 🧾 示例

```js
async function getData() {
  try {
    const result = await new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve("data");
      }, 1000);
    });
    console.log(result);
  } catch (error) {
    console.error(error);
  }
}
```

###  ✅正确认识 `async/await`

#### 基本特性

- `await` 表达式本质上是 **暂停执行直到 Promise 解决（fulfilled 或 rejected）**

- 所以**它看起来更像同步写法**（用同步代码的try catch代替catch，用await代替then），但**本质仍然是异步**（基于 Promise）

- `try/catch` 块**等价于** `.then().catch()` 的写法，但更清晰

  ```javascript
  // Promise
  fetch(url)
    .then(res => res.json())
    .then(data => doSomething(data))
    .catch(err => handleError(err));
  
  // async/await
  async function loadData(){
   try {
     const res = await fetch(url); 
     const data = await res.json();
     doSomething(data);
   } catch (err) {
     handleError(err);
   }
  } 
  ```

  

### ✅ 优点

- 写法像同步代码，可读性高
- 错误处理通过 `try/catch`，一致性好
- 更适合复杂逻辑、流程控制

---

## 🔁 三种方式对照

| 特性                     | Callback                      | Promise                         | async/await                       |
|--------------------------|-------------------------------|----------------------------------|-----------------------------------|
| 写法风格                 | 函数嵌套                      | 链式调用 `.then().catch()`      | 类同步，`await` + `try/catch`     |
| 可读性                   | 差，易陷入嵌套                | 中等，清晰但仍然链式            | 高，非常清晰                     |
| 错误处理                 | 手动传递错误                  | `.catch()`                      | `try/catch`                       |
| 并发操作                 | 麻烦                          | `Promise.all()`                 | `await Promise.all()` 支持更好   |
| 调试支持                 | 较差                          | 一般                            | 最好，配合 IDE 支持               |
| 适合场景                 | 简单异步操作                  | 中等复杂度、多级依赖            | 复杂控制流、依赖处理、流程逻辑   |

---

## ✅ 使用建议

| 使用场景                        | 推荐方式         |
|---------------------------------|------------------|
| 简单异步执行（小工具函数）      | Callback（谨慎） |
| 中等异步逻辑 + 错误处理         | Promise           |
| 复杂逻辑、多重依赖、流程控制     | async/await       |
| 多请求并发（批量加载数据）      | async + `Promise.all()` |
| 旧代码改造                      | Callback → Promise → async/await |

---

## 🧠 延伸理解：Promise 是铁路模型

- `.then()` 是一个轨道段，返回值是新的 Promise
- `.catch()` 是“错误轨道”
- `async/await` 是 Promise 的语法糖，让你写出同步风格的异步逻辑

---

## 📝 小结

```js
// 回调
fs.readFile("file.txt", (err, data) => {
  if (err) throw err;
  console.log(data);
});

// Promise
fs.promises.readFile("file.txt")
  .then(data => console.log(data))
  .catch(err => console.error(err));

// async/await
async function read() {
  try {
    const data = await fs.promises.readFile("file.txt");
    console.log(data);
  } catch (e) {
    console.error(e);
  }
}
```


---

# 🔧 Promise 的 `.catch()` 与自动包装机制

## ✅ `.catch()` 是 `.then(null, onRejected)` 的语法糖

```js
Promise.reject("发生错误")
  .catch(err => {
    console.log("捕获到错误:", err);
    return "恢复后的值";
  })
  .then(result => {
    console.log("继续执行:", result);  // 打印 "继续执行: 恢复后的值"
  });
```

### 🔍 等效写法

```js
promise.catch(err => handle(err));
```

等价于：

```js
promise.then(null, err => handle(err));
```

---

## 📦 自动包装行为总结

| 返回内容             | Promise 自动处理行为              |
|----------------------|-----------------------------------|
| 返回普通值           | 自动包装成 `Promise.resolve(value)` |
| 返回另一个 Promise   | 链接这个 Promise，等待它完成       |
| 没有返回（即 `undefined`） | 返回 `Promise.resolve(undefined)` |

---

## 🔁 链式结构示意图例

```js
Promise.reject("err")
  .catch(e => {
    // 异常轨道
    return 123; // 自动转回正轨，变成 Promise.resolve(123)
  })
  .then(v => {
    console.log(v); // 输出 123
  });
```

---

## ✅ 总结

> `.catch()` 本质是 `.then(null, onRejected)`，也会自动包装返回值为 Promise，完全是 Promise 链的一部分，允许你在出错后“恢复轨道”继续执行。

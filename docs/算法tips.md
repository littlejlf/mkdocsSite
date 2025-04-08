##### 涉及删除头结点
 如果遇到需要删除头节点的题目，添加哨兵节点可以简化代码逻辑，请记住这个技巧。 删除node结点 pre.next = pre.next.next node的前驱为pre head没有前驱 所以要加一个哨兵结点 ；头插法反转链表，也可以加一个哨兵结点，或者用None代替（不是子链表）
##### O(1)时间复杂度去删除和增加结点 使用双端链表


##### 回溯
![Alt text](images/%E7%AE%97%E6%B3%95tips/image.png)
![Alt text](images/%E7%AE%97%E6%B3%95tips/image-1.png)
[参考：算法随想录](https://programmercarl.com/%E5%9B%9E%E6%BA%AF%E7%AE%97%E6%B3%95%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80.html#%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80)
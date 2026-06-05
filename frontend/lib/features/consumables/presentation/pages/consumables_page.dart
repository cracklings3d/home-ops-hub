import 'package:flutter/material.dart';

/// Consumables management page.
class ConsumablesPage extends StatelessWidget {
  const ConsumablesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('耗材管理')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              const Icon(Icons.warning_amber, color: Colors.red, size: 20),
              const SizedBox(width: 8),
              const Text('5 个耗材库存不足', style: TextStyle(color: Colors.red, fontWeight: FontWeight.w600)),
              const Spacer(),
              TextButton(onPressed: () {}, child: const Text('查看全部')),
            ],
          ),
          const SizedBox(height: 12),
          ...List.generate(5, (i) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Colors.orange.shade50,
                child: const Icon(Icons.shopping_cart, color: Colors.orange),
              ),
              title: Text(['净水器滤芯', '空气净化器滤芯', '空调滤网', '吸尘器滤芯', '净水器滤芯'][i]),
              subtitle: Text('库存 0~1 / 需要 1~2', style: const TextStyle(fontSize: 12)),
              trailing: OutlinedButton(
                onPressed: () {},
                child: const Text('采购'),
              ),
            ),
          )),
          const SizedBox(height: 24),
          const Text('所有耗材', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
          const SizedBox(height: 12),
          ...List.generate(6, (i) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: const Icon(Icons.inventory_2_outlined),
              title: Text(['净水器滤芯', '空气净化器滤芯', '空调滤网', '戴森吸尘器滤芯', '洗衣机清洁剂', '油烟机滤网'][i]),
              subtitle: Text(['小米 H600G · 库存 1', '小米 AC-M15 · 库存 0', '格力通用 · 库存 2', '戴森 V15 · 库存 1', '通用 · 库存 3', '老板 8355 · 库存 0'][i]),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          )),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.add),
        label: const Text('添加耗材'),
      ),
    );
  }
}
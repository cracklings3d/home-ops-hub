import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AssetsPage extends StatelessWidget {
  const AssetsPage({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: Fetch from API
    final assets = [
      {'id': '1', 'name': '格力空调 KFR-35', 'brand': '格力', 'model': 'KFR-35GW', 'location': '客厅', 'status': 'normal'},
      {'id': '2', 'name': '小米净水器', 'brand': '小米', 'model': 'H600G', 'location': '厨房', 'status': 'normal'},
      {'id': '3', 'name': '老板油烟机', 'brand': '老板', 'model': '8355', 'location': '厨房', 'status': 'under_repair'},
      {'id': '4', 'name': '戴森吸尘器', 'brand': '戴森', 'model': 'V15', 'location': '储物间', 'status': 'normal'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('资产管理'),
        actions: [
          IconButton(
            icon: const Icon(Icons.qr_code_scanner),
            onPressed: () {},
            tooltip: '扫码',
          ),
        ],
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: const InputDecoration(
                hintText: '搜索资产...',
                prefixIcon: Icon(Icons.search),
              ),
              onChanged: (value) {},
            ),
          ),

          // Asset list
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: assets.length,
              itemBuilder: (context, index) {
                final asset = assets[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: asset['status'] == 'normal'
                          ? Colors.green.shade100
                          : Colors.orange.shade100,
                      child: Icon(
                        asset['status'] == 'normal' ? Icons.inventory_2 : Icons.build,
                        color: asset['status'] == 'normal' ? Colors.green : Colors.orange,
                      ),
                    ),
                    title: Text(asset['name'] as String),
                    subtitle: Text('${asset['brand']} · ${asset['location']}'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => context.push('/assets/${asset['id']}'),
                  ),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/assets/new'),
        icon: const Icon(Icons.add),
        label: const Text('添加资产'),
      ),
    );
  }
}
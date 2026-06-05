import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Asset detail page showing full information and related records.
class AssetDetailPage extends StatelessWidget {
  final String assetId;

  const AssetDetailPage({super.key, required this.assetId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('资产详情'),
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.pop()),
        actions: [
          IconButton(icon: const Icon(Icons.edit), onPressed: () => context.push('/assets/$assetId/edit')),
          IconButton(icon: const Icon(Icons.qr_code), onPressed: () {}),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Asset header
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  const Icon(Icons.inventory_2, size: 64, color: Colors.blue),
                  const SizedBox(height: 12),
                  Text('格力空调 KFR-35', style: Theme.of(context).textTheme.headlineSmall),
                  const SizedBox(height: 4),
                  Chip(
                    label: const Text('正常'),
                    backgroundColor: Colors.green.shade100,
                    labelStyle: const TextStyle(color: Colors.green),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Basic info
          _InfoSection(
            title: '基本信息',
            items: const [
              {'label': '品牌', 'value': '格力'},
              {'label': '型号', 'value': 'KFR-35GW/NhAe3Bj'},
              {'label': '序列号', 'value': 'LG20240605123'},
              {'label': '购买日期', 'value': '2024-06-05'},
              {'label': '保修截止', 'value': '2026-06-05'},
              {'label': '存放位置', 'value': '客厅'},
            ],
          ),
          const SizedBox(height: 16),

          // Quick actions
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.build),
                  label: const Text('维修记录'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.description),
                  label: const Text('文档'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.shopping_cart),
                  label: const Text('耗材'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Maintenance history
          _InfoSection(
            title: '维修记录',
            trailing: TextButton(onPressed: () {}, child: const Text('添加')),
            items: const [
              {'label': '2025-12-20', 'value': '更换遥控器电池 · ¥20'},
              {'label': '2025-08-15', 'value': '深度清洗 · ¥150'},
            ],
          ),
          const SizedBox(height: 16),

          // Documents
          _InfoSection(
            title: '相关文档',
            trailing: TextButton(onPressed: () {}, child: const Text('上传')),
            items: const [
              {'label': '说明书.pdf', 'value': '2024-06-05 上传'},
              {'label': '发票.jpg', 'value': '2024-06-05 上传'},
            ],
          ),
          const SizedBox(height: 16),

          // Purchase link
          Card(
            child: ListTile(
              leading: const Icon(Icons.shopping_bag),
              title: const Text('购买链接'),
              subtitle: const Text('京东 - 格力空调官方旗舰店'),
              trailing: const Icon(Icons.open_in_new),
              onTap: () {},
            ),
          ),
          const SizedBox(height: 16),

          // Notes
          Card(
            child: const ListTile(
              leading: Icon(Icons.note),
              title: Text('备注'),
              subtitle: Text('2024年6月购买，质保期2年。'),
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoSection extends StatelessWidget {
  final String title;
  final Widget? trailing;
  final List<Map<String, String>> items;

  const _InfoSection({required this.title, this.trailing, required this.items});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: Theme.of(context).textTheme.titleMedium),
                if (trailing != null) trailing!,
              ],
            ),
            const SizedBox(height: 12),
            ...items.map((item) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(
                        width: 80,
                        child: Text(item['label']!, style: const TextStyle(color: Colors.grey, fontSize: 13)),
                      ),
                      Expanded(child: Text(item['value']!, style: const TextStyle(fontSize: 13))),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }
}
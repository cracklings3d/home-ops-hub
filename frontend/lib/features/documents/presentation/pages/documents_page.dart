import 'package:flutter/material.dart';

/// Documents management page.
class DocumentsPage extends StatelessWidget {
  const DocumentsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('文档管理')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            decoration: const InputDecoration(
              hintText: '搜索文档...',
              prefixIcon: Icon(Icons.search),
            ),
          ),
          const SizedBox(height: 16),
          const Text('按设备分类', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
          const SizedBox(height: 12),
          ...List.generate(3, (i) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ExpansionTile(
              leading: const Icon(Icons.inventory_2),
              title: Text(['格力空调 KFR-35 (3份)', '小米净水器 H600G (2份)', '老板油烟机 8355 (4份)'][i]),
              children: [
                ListTile(
                  leading: const Icon(Icons.picture_as_pdf, color: Colors.red),
                  title: const Text('使用说明书.pdf'),
                  subtitle: const Text('PDF · 2.3 MB · 2024-06-05'),
                  trailing: IconButton(icon: const Icon(Icons.download), onPressed: () {}),
                ),
                ListTile(
                  leading: const Icon(Icons.image, color: Colors.green),
                  title: const Text('发票.jpg'),
                  subtitle: const Text('图片 · 856 KB · 2024-06-05'),
                  trailing: IconButton(icon: const Icon(Icons.download), onPressed: () {}),
                ),
              ],
            ),
          )),
          const SizedBox(height: 24),
          const Text('最近上传', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
          const SizedBox(height: 12),
          ...List.generate(4, (i) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: Icon(
                [Icons.picture_as_pdf, Icons.image, Icons.description, Icons.picture_as_pdf][i],
                color: [Colors.red, Colors.green, Colors.blue, Colors.red][i],
              ),
              title: Text(['格力空调说明书.pdf', '发票_20240605.jpg', '维修工单_20250520.pdf', '净水器安装视频.mp4'][i]),
              subtitle: Text(['上传于 2024-06-05 · 2.3 MB', '上传于 2024-06-05 · 856 KB', '上传于 2025-05-20 · 120 KB', '上传于 2025-01-15 · 45 MB'][i]),
              trailing: const Icon(Icons.more_vert),
            ),
          )),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.upload_file),
        label: const Text('上传文档'),
      ),
    );
  }
}
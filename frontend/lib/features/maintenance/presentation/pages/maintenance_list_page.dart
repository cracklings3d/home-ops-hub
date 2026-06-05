import 'package:flutter/material.dart';

/// Maintenance records list page.
class MaintenanceListPage extends StatelessWidget {
  const MaintenanceListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('维修记录')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Quick add
          Card(
            child: ListTile(
              leading: const CircleAvatar(child: Icon(Icons.add)),
              title: const Text('添加维修记录'),
              subtitle: const Text('记录设备维修、更换配件等信息'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),
          const SizedBox(height: 16),
          // Records
          ...List.generate(3, (i) => Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Colors.blue.shade50,
                child: const Icon(Icons.build, color: Colors.blue),
              ),
              title: Text(['空调深度清洗', '净水器滤芯更换', '油烟机电机维修'][i]),
              subtitle: Text(['格力空调 KFR-35 · 2026-06-01', '小米净水器 H600G · 2026-05-20', '老板油烟机 8355 · 2026-04-15'][i]),
              trailing: Text(['¥150', '¥280', '¥320'][i], style: const TextStyle(fontWeight: FontWeight.w600)),
              onTap: () {},
            ),
          )),
        ],
      ),
      floatingActionButton: FloatingActionButton(onPressed: () {}, child: const Icon(Icons.add)),
    );
  }
}
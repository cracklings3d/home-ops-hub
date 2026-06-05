import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

/// Dashboard page showing overview of all home operations.
/// Provides quick access to key metrics and upcoming tasks.
class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('仪表盘'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Stats cards row
          Row(
            children: [
              Expanded(child: _StatCard(title: '总资产', value: '12', icon: Icons.inventory_2, color: Colors.blue)),
              const SizedBox(width: 12),
              Expanded(child: _StatCard(title: '待维修', value: '2', icon: Icons.build, color: Colors.orange)),
              const SizedBox(width: 12),
              Expanded(child: _StatCard(title: '低库存', value: '5', icon: Icons.warning, color: Colors.red)),
            ],
          ),
          const SizedBox(height: 20),

          // Asset status chart
          _SectionCard(
            title: '资产状态分布',
            child: SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(value: 8, title: '正常', color: Colors.green, radius: 60),
                    PieChartSectionData(value: 2, title: '维修中', color: Colors.orange, radius: 60),
                    PieChartSectionData(value: 2, title: '已报废', color: Colors.grey, radius: 60),
                  ],
                  centerSpaceRadius: 40,
                  sectionsSpace: 2,
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Upcoming maintenance
          _SectionCard(
            title: '近期维保提醒',
            trailing: TextButton(onPressed: () {}, child: const Text('查看全部')),
            child: Column(
              children: [
                _ReminderItem(
                  title: '空调滤网清洗',
                  asset: '格力空调 KFR-35',
                  dueDate: '2026-06-10',
                  isUrgent: false,
                ),
                const Divider(height: 1),
                _ReminderItem(
                  title: '净水器滤芯更换',
                  asset: '小米净水器 H600G',
                  dueDate: '2026-06-08',
                  isUrgent: true,
                ),
                const Divider(height: 1),
                _ReminderItem(
                  title: '油烟机滤网清洗',
                  asset: '老板油烟机 8355',
                  dueDate: '2026-06-15',
                  isUrgent: false,
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Low stock consumables
          _SectionCard(
            title: '待采购耗材',
            trailing: TextButton(onPressed: () {}, child: const Text('查看全部')),
            child: Column(
              children: [
                _ConsumableItem(name: '净水器滤芯', model: '小米 F7', stock: 1, needed: 2),
                const Divider(height: 1),
                _ConsumableItem(name: '空气净化器滤芯', model: '小米 AC-M15-SC', stock: 0, needed: 1),
                const Divider(height: 1),
                _ConsumableItem(name: '空调滤网', model: '格力 50526131', stock: 0, needed: 2),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(value, style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold)),
            Text(title, style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  final String title;
  final Widget? trailing;
  final Widget child;

  const _SectionCard({required this.title, this.trailing, required this.child});

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
                Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
                if (trailing != null) trailing!,
              ],
            ),
            const SizedBox(height: 16),
            child,
          ],
        ),
      ),
    );
  }
}

class _ReminderItem extends StatelessWidget {
  final String title;
  final String asset;
  final String dueDate;
  final bool isUrgent;

  const _ReminderItem({
    required this.title,
    required this.asset,
    required this.dueDate,
    required this.isUrgent,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: Icon(
        isUrgent ? Icons.warning_amber : Icons.schedule,
        color: isUrgent ? Colors.orange : Colors.grey,
      ),
      title: Text(title),
      subtitle: Text(asset, style: const TextStyle(fontSize: 12)),
      trailing: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        decoration: BoxDecoration(
          color: isUrgent ? Colors.red.shade50 : Colors.grey.shade100,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(dueDate, style: TextStyle(fontSize: 12, color: isUrgent ? Colors.red : Colors.grey)),
      ),
    );
  }
}

class _ConsumableItem extends StatelessWidget {
  final String name;
  final String model;
  final int stock;
  final int needed;

  const _ConsumableItem({
    required this.name,
    required this.model,
    required this.stock,
    required this.needed,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: const Icon(Icons.shopping_bag_outlined, color: Colors.blue),
      title: Text(name),
      subtitle: Text(model, style: const TextStyle(fontSize: 12)),
      trailing: Text(
        '$stock / $needed',
        style: TextStyle(
          color: stock == 0 ? Colors.red : Colors.orange,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
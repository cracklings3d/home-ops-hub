import 'package:flutter/material.dart';

/// Adaptive scaffold that shows bottom navigation on mobile,
/// side navigation rail on desktop/tablet.
class AppScaffold extends StatelessWidget {
  final Widget child;

  const AppScaffold({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final isWide = width >= 768;

    return Scaffold(
      body: Row(
        children: [
          if (isWide) _NavigationRail(),
          Expanded(child: child),
        ],
      ),
      bottomNavigationBar: isWide ? null : const _BottomNavBar(),
    );
  }
}

class _NavigationRail extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final currentPath = GoRouterState.of(context).uri.toString();
    int selectedIndex = 0;
    if (currentPath.startsWith('/dashboard')) selectedIndex = 0;
    if (currentPath.startsWith('/assets')) selectedIndex = 1;
    if (currentPath.startsWith('/maintenance')) selectedIndex = 2;
    if (currentPath.startsWith('/consumables')) selectedIndex = 3;
    if (currentPath.startsWith('/documents')) selectedIndex = 4;

    return NavigationRail(
      selectedIndex: selectedIndex,
      onDestinationSelected: (i) => _navigate(context, i),
      labelType: NavigationRailLabelType.all,
      leading: const Padding(
        padding: EdgeInsets.symmetric(vertical: 16),
        child: Icon(Icons.home_repair_service, size: 32, color: Color(0xFF2563EB)),
      ),
      destinations: const [
        NavigationRailDestination(
          icon: Icon(Icons.dashboard_outlined),
          selectedIcon: Icon(Icons.dashboard),
          label: Text('仪表盘'),
        ),
        NavigationRailDestination(
          icon: Icon(Icons.inventory_2_outlined),
          selectedIcon: Icon(Icons.inventory_2),
          label: Text('资产'),
        ),
        NavigationRailDestination(
          icon: Icon(Icons.build_outlined),
          selectedIcon: Icon(Icons.build),
          label: Text('维修'),
        ),
        NavigationRailDestination(
          icon: Icon(Icons.shopping_cart_outlined),
          selectedIcon: Icon(Icons.shopping_cart),
          label: Text('耗材'),
        ),
        NavigationRailDestination(
          icon: Icon(Icons.folder_outlined),
          selectedIcon: Icon(Icons.folder),
          label: Text('文档'),
        ),
      ],
    );
  }
}

class _BottomNavBar extends StatelessWidget {
  const _BottomNavBar();

  @override
  Widget build(BuildContext context) {
    final currentPath = GoRouterState.of(context).uri.toString();
    int selectedIndex = 0;
    if (currentPath.startsWith('/dashboard')) selectedIndex = 0;
    if (currentPath.startsWith('/assets')) selectedIndex = 1;
    if (currentPath.startsWith('/maintenance')) selectedIndex = 2;
    if (currentPath.startsWith('/consumables')) selectedIndex = 3;
    if (currentPath.startsWith('/documents')) selectedIndex = 4;

    return NavigationBar(
      selectedIndex: selectedIndex,
      onDestinationSelected: (i) => _navigate(context, i),
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.dashboard_outlined),
          selectedIcon: Icon(Icons.dashboard),
          label: '仪表盘',
        ),
        NavigationDestination(
          icon: Icon(Icons.inventory_2_outlined),
          selectedIcon: Icon(Icons.inventory_2),
          label: '资产',
        ),
        NavigationDestination(
          icon: Icon(Icons.build_outlined),
          selectedIcon: Icon(Icons.build),
          label: '维修',
        ),
        NavigationDestination(
          icon: Icon(Icons.shopping_cart_outlined),
          selectedIcon: Icon(Icons.shopping_cart),
          label: '耗材',
        ),
        NavigationDestination(
          icon: Icon(Icons.folder_outlined),
          selectedIcon: Icon(Icons.folder),
          label: '文档',
        ),
      ],
    );
  }
}

void _navigate(BuildContext context, int index) {
  final routes = ['/dashboard', '/assets', '/maintenance', '/consumables', '/documents'];
  context.go(routes[index]);
}
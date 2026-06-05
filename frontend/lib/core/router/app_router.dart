import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';

import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/assets/presentation/pages/assets_page.dart';
import '../../features/assets/presentation/pages/asset_detail_page.dart';
import '../../features/assets/presentation/pages/asset_form_page.dart';
import '../../features/maintenance/presentation/pages/maintenance_list_page.dart';
import '../../features/consumables/presentation/pages/consumables_page.dart';
import '../../features/documents/presentation/pages/documents_page.dart';
import '../../shared/widgets/app_scaffold.dart';

/// App router configuration using go_router.
/// Supports mobile (bottom nav) and desktop (side nav) layouts.
class AppRouter {
  AppRouter._();

  static final GlobalKey<NavigatorState> _rootNavigatorKey =
      GlobalKey<NavigatorState>(debugLabel: 'root');
  static final GlobalKey<NavigatorState> _shellNavigatorKey =
      GlobalKey<NavigatorState>(debugLabel: 'shell');

  static final GoRouter router = GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: '/dashboard',
    debugLogDiagnostics: true,
    routes: [
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => AppScaffold(child: child),
        routes: [
          GoRoute(
            path: '/dashboard',
            name: 'dashboard',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: DashboardPage(),
            ),
          ),
          GoRoute(
            path: '/assets',
            name: 'assets',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: AssetsPage(),
            ),
            routes: [
              GoRoute(
                path: 'new',
                name: 'asset-new',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) => const AssetFormPage(),
              ),
              GoRoute(
                path: ':id',
                name: 'asset-detail',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) {
                  final id = state.pathParameters['id']!;
                  return AssetDetailPage(assetId: id);
                },
                routes: [
                  GoRoute(
                    path: 'edit',
                    name: 'asset-edit',
                    parentNavigatorKey: _rootNavigatorKey,
                    builder: (context, state) {
                      final id = state.pathParameters['id']!;
                      return AssetFormPage(assetId: id);
                    },
                  ),
                ],
              ),
            ],
          ),
          GoRoute(
            path: '/maintenance',
            name: 'maintenance',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: MaintenanceListPage(),
            ),
          ),
          GoRoute(
            path: '/consumables',
            name: 'consumables',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: ConsumablesPage(),
            ),
          ),
          GoRoute(
            path: '/documents',
            name: 'documents',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: DocumentsPage(),
            ),
          ),
        ],
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Page not found: ${state.uri}'),
      ),
    ),
  );
}
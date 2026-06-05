import 'package:flutter_test/flutter_test.dart';

import 'package:home_ops_hub/models/asset.dart';

void main() {
  group('Asset Model', () {
    test('fromJson creates valid Asset', () {
      final json = {
        'id': '123e4567-e89b-12d3-a456-426614174000',
        'name': '格力空调',
        'brand': '格力',
        'model': 'KFR-35GW',
        'serial_number': 'LG20240605001',
        'purchase_date': '2024-06-05',
        'warranty_end': '2026-06-05',
        'location': '客厅',
        'category': '1',
        'category_name': '空调',
        'purchase_link': 'https://jd.com/item/123',
        'notes': '测试备注',
        'qr_code': 'asset-123',
        'photos': ['https://example.com/photo1.jpg'],
        'status': 'normal',
        'maintenance_count': 2,
        'document_count': 3,
        'created_at': '2024-06-05T10:30:00Z',
        'updated_at': '2024-06-05T10:30:00Z',
      };

      final asset = Asset.fromJson(json);

      expect(asset.id, '123e4567-e89b-12d3-a456-426614174000');
      expect(asset.name, '格力空调');
      expect(asset.brand, '格力');
      expect(asset.model, 'KFR-35GW');
      expect(asset.serialNumber, 'LG20240605001');
      expect(asset.location, '客厅');
      expect(asset.status, AssetStatus.normal);
      expect(asset.maintenanceCount, 2);
      expect(asset.photos.length, 1);
    });

    test('isUnderWarranty returns true when warranty is in future', () {
      final futureDate = DateTime.now().add(const Duration(days: 30));
      final asset = Asset(
        id: '1',
        name: '测试设备',
        brand: '品牌',
        model: '型号',
        warrantyEnd: futureDate,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(asset.isUnderWarranty, true);
    });

    test('isUnderWarranty returns false when warranty is expired', () {
      final pastDate = DateTime.now().subtract(const Duration(days: 30));
      final asset = Asset(
        id: '1',
        name: '测试设备',
        brand: '品牌',
        model: '型号',
        warrantyEnd: pastDate,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(asset.isUnderWarranty, false);
    });

    test('toJson produces correct map', () {
      final asset = Asset(
        id: '123',
        name: '测试空调',
        brand: '格力',
        model: 'KFR-35',
        purchaseDate: DateTime(2024, 6, 5),
        warrantyEnd: DateTime(2026, 6, 5),
        location: '客厅',
        status: AssetStatus.normal,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      final json = asset.toJson();

      expect(json['id'], '123');
      expect(json['name'], '测试空调');
      expect(json['brand'], '格力');
      expect(json['model'], 'KFR-35');
      expect(json['location'], '客厅');
      expect(json['status'], 'normal');
      expect(json['purchase_date'], '2024-06-05');
      expect(json['warranty_end'], '2026-06-05');
    });
  });

  group('AssetCategory Model', () {
    test('fromJson creates valid AssetCategory', () {
      final json = {
        'id': 'cat-1',
        'name': '厨房电器',
        'icon': 'kitchen',
        'color': '#2563EB',
        'asset_count': 5,
        'sort_order': 1,
      };

      final category = AssetCategory.fromJson(json);

      expect(category.id, 'cat-1');
      expect(category.name, '厨房电器');
      expect(category.assetCount, 5);
      expect(category.sortOrder, 1);
    });
  });

  group('AssetStatus', () {
    test('fromString returns correct status', () {
      expect(AssetStatus.fromString('normal'), AssetStatus.normal);
      expect(AssetStatus.fromString('under_repair'), AssetStatus.underRepair);
      expect(AssetStatus.fromString('retired'), AssetStatus.retired);
      expect(AssetStatus.fromString('unknown'), AssetStatus.normal);
    });

    test('status values and labels are correct', () {
      expect(AssetStatus.normal.value, 'normal');
      expect(AssetStatus.normal.label, '正常');
      expect(AssetStatus.underRepair.value, 'under_repair');
      expect(AssetStatus.underRepair.label, '维修中');
      expect(AssetStatus.retired.value, 'retired');
      expect(AssetStatus.retired.label, '已报废');
    });
  });
}
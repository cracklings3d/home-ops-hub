import 'package:equatable/equatable.dart';

/// Represents a home asset/equipment in the system.
class Asset extends Equatable {
  final String id;
  final String name;
  final String brand;
  final String model;
  final String? serialNumber;
  final DateTime? purchaseDate;
  final DateTime? warrantyEnd;
  final String? location;
  final String? categoryId;
  final String? categoryName;
  final String? purchaseLink;
  final String? notes;
  final String? qrCode;
  final List<String> photos;
  final AssetStatus status;
  final int maintenanceCount;
  final int documentCount;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Asset({
    required this.id,
    required this.name,
    required this.brand,
    required this.model,
    this.serialNumber,
    this.purchaseDate,
    this.warrantyEnd,
    this.location,
    this.categoryId,
    this.categoryName,
    this.purchaseLink,
    this.notes,
    this.qrCode,
    this.photos = const [],
    this.status = AssetStatus.normal,
    this.maintenanceCount = 0,
    this.documentCount = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  bool get isUnderWarranty {
    if (warrantyEnd == null) return false;
    return warrantyEnd!.isAfter(DateTime.now());
  }

  int get daysUntilWarrantyExpires {
    if (warrantyEnd == null) return -1;
    return warrantyEnd!.difference(DateTime.now()).inDays;
  }

  factory Asset.fromJson(Map<String, dynamic> json) {
    return Asset(
      id: json['id'] as String,
      name: json['name'] as String,
      brand: json['brand'] as String,
      model: json['model'] as String,
      serialNumber: json['serial_number'] as String?,
      purchaseDate: json['purchase_date'] != null
          ? DateTime.parse(json['purchase_date'] as String)
          : null,
      warrantyEnd: json['warranty_end'] != null
          ? DateTime.parse(json['warranty_end'] as String)
          : null,
      location: json['location'] as String?,
      categoryId: json['category']?.toString(),
      categoryName: json['category_name'] as String?,
      purchaseLink: json['purchase_link'] as String?,
      notes: json['notes'] as String?,
      qrCode: json['qr_code'] as String?,
      photos: (json['photos'] as List<dynamic>?)?.cast<String>() ?? [],
      status: AssetStatus.fromString(json['status'] as String? ?? 'normal'),
      maintenanceCount: json['maintenance_count'] as int? ?? 0,
      documentCount: json['document_count'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'brand': brand,
        'model': model,
        'serial_number': serialNumber,
        'purchase_date': purchaseDate?.toIso8601String().split('T').first,
        'warranty_end': warrantyEnd?.toIso8601String().split('T').first,
        'location': location,
        'category': categoryId,
        'purchase_link': purchaseLink,
        'notes': notes,
        'status': status.value,
      };

  @override
  List<Object?> get props => [id, name, brand, model, status];
}

enum AssetStatus {
  normal('normal', '正常'),
  underRepair('under_repair', '维修中'),
  retired('retired', '已报废');

  final String value;
  final String label;
  const AssetStatus(this.value, this.label);

  static AssetStatus fromString(String value) {
    return AssetStatus.values.firstWhere(
      (e) => e.value == value,
      orElse: () => AssetStatus.normal,
    );
  }
}

/// Category for organizing assets.
class AssetCategory extends Equatable {
  final String id;
  final String name;
  final String? icon;
  final String? color;
  final int assetCount;
  final int sortOrder;

  const AssetCategory({
    required this.id,
    required this.name,
    this.icon,
    this.color,
    this.assetCount = 0,
    this.sortOrder = 0,
  });

  factory AssetCategory.fromJson(Map<String, dynamic> json) {
    return AssetCategory(
      id: json['id'] as String,
      name: json['name'] as String,
      icon: json['icon'] as String?,
      color: json['color'] as String?,
      assetCount: json['asset_count'] as int? ?? 0,
      sortOrder: json['sort_order'] as int? ?? 0,
    );
  }

  @override
  List<Object?> get props => [id, name];
}
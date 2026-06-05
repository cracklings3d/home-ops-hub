import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Asset create/edit form page.
class AssetFormPage extends StatefulWidget {
  final String? assetId;

  const AssetFormPage({super.key, this.assetId});

  @override
  State<AssetFormPage> createState() => _AssetFormPageState();
}

class _AssetFormPageState extends State<AssetFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  final _brandCtrl = TextEditingController();
  final _modelCtrl = TextEditingController();
  final _serialCtrl = TextEditingController();
  final _locationCtrl = TextEditingController();
  final _purchaseLinkCtrl = TextEditingController();
  final _notesCtrl = TextEditingController();

  DateTime? _purchaseDate;
  DateTime? _warrantyEnd;
  String? _categoryValue;

  bool get isEditing => widget.assetId != null;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(isEditing ? '编辑资产' : '添加资产'),
        leading: IconButton(icon: const Icon(Icons.close), onPressed: () => context.pop()),
        actions: [
          TextButton(onPressed: _save, child: const Text('保存')),
        ],
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text('基本信息', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            TextFormField(
              controller: _nameCtrl,
              decoration: const InputDecoration(labelText: '设备名称 *', hintText: '例如：格力空调'),
              validator: (v) => v == null || v.isEmpty ? '请输入设备名称' : null,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: TextFormField(controller: _brandCtrl, decoration: const InputDecoration(labelText: '品牌'))),
                const SizedBox(width: 12),
                Expanded(child: TextFormField(controller: _modelCtrl, decoration: const InputDecoration(labelText: '型号'))),
              ],
            ),
            const SizedBox(height: 12),
            TextFormField(controller: _serialCtrl, decoration: const InputDecoration(labelText: '序列号')),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _categoryValue,
              decoration: const InputDecoration(labelText: '分类'),
              items: const [
                DropdownMenuItem(value: 'kitchen', child: Text('厨房')),
                DropdownMenuItem(value: 'living', child: Text('客厅')),
                DropdownMenuItem(value: 'bedroom', child: Text('卧室')),
                DropdownMenuItem(value: 'bathroom', child: Text('卫生间')),
                DropdownMenuItem(value: 'garage', child: Text('车库')),
              ],
              onChanged: (v) => setState(() => _categoryValue = v),
            ),
            const SizedBox(height: 12),
            TextFormField(controller: _locationCtrl, decoration: const InputDecoration(labelText: '存放位置')),
            const SizedBox(height: 24),
            const Text('购买信息', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _DateField(
                    label: '购买日期',
                    value: _purchaseDate,
                    onChanged: (d) => setState(() => _purchaseDate = d),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _DateField(
                    label: '保修截止',
                    value: _warrantyEnd,
                    onChanged: (d) => setState(() => _warrantyEnd = d),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            TextFormField(controller: _purchaseLinkCtrl, decoration: const InputDecoration(labelText: '购买链接')),
            const SizedBox(height: 24),
            const Text('其他', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            TextFormField(controller: _notesCtrl, decoration: const InputDecoration(labelText: '备注'), maxLines: 3),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _save,
              icon: const Icon(Icons.check),
              label: Text(isEditing ? '保存更改' : '创建资产'),
            ),
          ],
        ),
      ),
    );
  }

  void _save() {
    if (_formKey.currentState?.validate() ?? false) {
      // TODO: Save to API
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(isEditing ? '已保存' : '已创建')));
      context.pop();
    }
  }
}

class _DateField extends StatelessWidget {
  final String label;
  final DateTime? value;
  final ValueChanged<DateTime?> onChanged;

  const _DateField({required this.label, required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () async {
        final date = await showDatePicker(
          context: context,
          initialDate: value ?? DateTime.now(),
          firstDate: DateTime(2000),
          lastDate: DateTime(2100),
        );
        onChanged(date);
      },
      child: InputDecorator(
        decoration: InputDecoration(labelText: label),
        child: Text(
          value != null ? '${value!.year}-${value!.month.toString().padLeft(2, '0')}-${value!.day.toString().padLeft(2, '0')}' : '选择日期',
          style: TextStyle(color: value != null ? null : Colors.grey),
        ),
      ),
    );
  }
}
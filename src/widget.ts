import { ISerializers, WidgetView } from '@jupyter-widgets/base';
import { DropdownModel, DropdownView } from '@jupyter-widgets/controls';

import { MODULE_NAME, MODULE_VERSION } from './version';

export
class DropdownExtendedModel extends DropdownModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: DropdownExtendedModel.model_name,
            _model_module: DropdownExtendedModel.model_module,
            _model_module_version: DropdownExtendedModel.model_module_version,
            _view_name: DropdownExtendedModel.view_name,
            _view_module: DropdownExtendedModel.view_module,
            _view_module_version: DropdownExtendedModel.view_module_version,
        };
    }

    static serializers: ISerializers = {...DropdownModel.serializers}

    static model_name = 'DropdownExtendedModel';
    static model_module = MODULE_NAME;
    static model_module_version = MODULE_VERSION;
    static view_name = 'DropdownExtendedView';
    static view_module = MODULE_NAME;
    static view_module_version = MODULE_VERSION;
}

export
class DropdownExtendedView extends DropdownView {
    initialize(parameters: WidgetView.InitializeParameters): void {
        super.initialize(parameters);
        this.listenTo(this.model, 'change:_disabled_options_labels', () => this._updateOptions());
    }

    _updateOptions(): void {
        this.listbox.textContent = '';
        const items = this.model.get('_options_labels');
        const disabled_items = this.model.get('_disabled_options_labels');
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            const option = document.createElement('option');
            option.textContent = item.replace(/ /g, '\xa0'); // space -> &nbsp;
            option.setAttribute('data-value', encodeURIComponent(item));
            option.disabled = disabled_items.includes(item);
            option.value = item;
            this.listbox.appendChild(option);
        }
    }
}

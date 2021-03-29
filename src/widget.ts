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
        this.listenTo(this.model, 'change:_grouping_labels', () => this._updateOptions());
    }

    _updateOptions(): void {
        this.listbox.textContent = '';
        const grouping = this.model.get('_grouping_labels');
        const items = this.model.get('_options_labels');
        const disabled_items = this.model.get('_disabled_options_labels');
        if (grouping && grouping.length) {
            for (let i = 0; i < grouping.length; i++) {
                const header = grouping[i][0];
                if (header) { this._updateOptionsUtility(header, true, true); }
                for (let j = 0; j < grouping[i][1].length; j++) {
                    let item = grouping[i][1][j];
                    if (header) { item = ' ' + item; }
                    const disabled = disabled_items.includes(grouping[i][1][j]);
                    this._updateOptionsUtility(item, disabled, false);
                }
            }
        } else {
            for (let i = 0; i < items.length; i++) {
                const item = items[i];
                const disabled = disabled_items.includes(item);
                this._updateOptionsUtility(item, disabled, false);
            }
        }
    }

    _updateOptionsUtility(item: string, disabled: boolean, bold_and_black: boolean): void {
        const option = document.createElement('option');
        option.textContent = item.replace(/ /g, '\xa0'); // space -> &nbsp; (no-break space)
        if (bold_and_black) {
            option.style.fontWeight = 'bold';
            option.style.color = 'black';
        }
        option.setAttribute('data-value', encodeURIComponent(item));
        option.disabled = disabled;
        option.value = item;
        this.listbox.appendChild(option);
    }
}

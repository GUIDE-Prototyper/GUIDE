import iconData from './icons.json';

interface Icon {
    iconName: string;
    type: string;
    id: string;
    key: string;
}

const icons: Icon[] = iconData.icons;

function findIconByName(iconName: string): Icon | undefined {
    return icons.find(icon => icon.iconName === iconName);
}

export function getKeyByIconName(iconName: string): string {

    const icon = findIconByName(iconName);
    if (icon != undefined){
        if (icon.type == 'custo_mat'){
            return '59e9a919748e34d7ec272d73644d115c92e652b3'
        }
       return icon.key;
    } 
    return '59e9a919748e34d7ec272d73644d115c92e652b3'
}

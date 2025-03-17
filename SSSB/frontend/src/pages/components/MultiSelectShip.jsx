import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

// const names = [
//   'Oliver Hansen',
//   'Van Henry',
//   'April Tucker',
//   'Ralph Hubbard',
//   'Omar Alexander',
//   'Carlos Abbott',
//   'Miriam Wagner',
//   'Bradley Wilkerson',
//   'Virginia Andrews',
//   'Kelly Snyder',
// ];

function getStyles(name, personName, theme) {
  return {
    fontWeight: personName.includes(name)
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

function MultipleSelectChip({ options = [], label = 'Chip', width = 300, value = [], onValueChange, disabled = false }) {
  const theme = useTheme();
  const [personName, setPersonName] = React.useState(value);

  React.useEffect(() => {
    setPersonName(value);
  }, [value]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    const newValue = typeof value === 'string' ? value.split(',') : value;
    setPersonName(newValue);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  const handleDelete = (chipToDelete) => () => {
    const newValue = personName.filter((name) => name !== chipToDelete);
    setPersonName(newValue);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  return (
    <FormControl sx={{ width }}>
      <InputLabel id="multiple-chip-label">{label}</InputLabel>
      <Select
        labelId="multiple-chip-label"
        id="multiple-chip"
        multiple
        value={personName}
        onChange={handleChange}
        disabled={disabled}
        input={<OutlinedInput id="select-multiple-chip" label={label} />}
        renderValue={(selected) => {
          return (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip
                  key={value}
                  label={value}
                  onDelete={handleDelete(value)}
                  onMouseDown={(event) => event.stopPropagation()}
                />
              ))}
            </Box>
          );
        }}

        MenuProps={MenuProps}
      >
        <MenuItem disabled value="">
          <em>Not Specified</em>
        </MenuItem>
        {options.map((name) => (
          <MenuItem
            key={name}
            value={name}
            style={getStyles(name, personName, theme)}
          >
            {name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

export default MultipleSelectChip;
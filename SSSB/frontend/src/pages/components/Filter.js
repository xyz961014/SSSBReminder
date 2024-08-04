import * as React from 'react';
import { useEffect, useState } from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/system';

const FormGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

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

export default function Filter() {
  const theme = useTheme();
  const [regions, setRegions] = useState([]);
  const [types, setTypes] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState([]);
  const [selectedType, setSelectedType] = useState([]);
  const [spaceRange, setSpaceRange] = useState([0, 100]);
  const [rentRange, setRentRange] = useState([0, 10000]);
  const [creditRange, setCreditRange] = useState([0, 1000]);

  const handleSpaceRangeChange = (event, newValue) => {
    setSpaceRange(newValue);
  };

  const handleRentRangeChange = (event, newValue) => {
    setRentRange(newValue);
  };

  const handleCreditRangeChange = (event, newValue) => {
    setCreditRange(newValue);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // const response = await axios.get('https://api.example.com/data');
        const regions = [
          'Strix',
          'Lappis',
          'Forum',
          'XXX',
        ];
        setRegions(regions);
        const types = [
          "Studio",
          "Apartment",
          "Corridor",
        ];
        setTypes(types);
      } catch (err) {
      }
    };

    fetchData();
  }, []);

  const handleRegionChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedRegion(value);
  };

  const handleTypeChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedType(value);
  };

  return (
    <React.Fragment>
      <Grid container spacing={2}>
        <FormGrid item xs={12}>
          <FormLabel htmlFor="region">
            Region
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Select
              labelId="demo-multiple-chip-label"
              id="demo-multiple-chip"
              multiple
              value={selectedRegion}
              onChange={handleRegionChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value} />
                  ))}
                </Box>
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              {regions.map((region) => (
                <MenuItem
                  key={region}
                  value={region}
                >
                  {region}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}}>
              Select All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="type">
            Accomodation Type
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Select
              labelId="demo-multiple-chip-label"
              id="demo-multiple-chip"
              multiple
              value={selectedType}
              onChange={handleTypeChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value} />
                  ))}
                </Box>
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              {types.map((type) => (
                <MenuItem
                  key={type}
                  value={type}
                >
                  {type}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}}>
              Select All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="space">
            Living Space
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Living space range'}
              value={spaceRange}
              onChange={handleSpaceRangeChange}
              valueLabelDisplay="on"
              min={0}
              max={200}
              sx={{ mt: 5 }}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="rent">
            Rent
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Rent range'}
              value={rentRange}
              onChange={handleRentRangeChange}
              valueLabelDisplay="on"
              min={0}
              max={20000}
              sx={{ mt: 5 }}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="credit">
            Credit Days Required
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Credit days range'}
              value={creditRange}
              onChange={handleCreditRangeChange}
              valueLabelDisplay="on"
              min={0}
              max={3000}
              sx={{ mt: 5 }}
            />
          </Box>
        </FormGrid>

        {/*
        <FormGrid item xs={12}>
          <FormLabel htmlFor="distance to">
            Distance To
          </FormLabel>
          <OutlinedInput
            id="last-name"
            name="last-name"
            type="last-name"
            placeholder="Snow"
            autoComplete="last name"
            required
          />
        </FormGrid>
        */}

      </Grid>
    </React.Fragment>
  );
}

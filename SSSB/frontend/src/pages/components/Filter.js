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
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/system';

import { fetchRegions, fetchTypes, fetchSpaceRange, fetchRentRange, fetchFloorRange, fetchCreditRange } from '../../Api'

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

  const [spaceMin, setSpaceMin] = useState(0);
  const [spaceMax, setSpaceMax] = useState(200);
  const [spaceRange, setSpaceRange] = useState([0, 100]);

  const [rentMin, setRentMin] = useState(0);
  const [rentMax, setRentMax] = useState(20000);
  const [rentRange, setRentRange] = useState([0, 10000]);

  const [floorMin, setFloorMin] = useState(-5);
  const [floorMax, setFloorMax] = useState(25);
  const [floorRange, setFloorRange] = useState([0, 10000]);

  const [creditMin, setCreditMin] = useState(0);
  const [creditMax, setCreditMax] = useState(2000);
  const [creditRange, setCreditRange] = useState([0, 1000]);

  const handleSpaceRangeChange = (event, newValue) => {
    setSpaceRange(newValue);
  };

  const handleRentRangeChange = (event, newValue) => {
    setRentRange(newValue);
  };

  const handleFloorRangeChange = (event, newValue) => {
    setFloorRange(newValue);
  };

  const handleCreditRangeChange = (event, newValue) => {
    setCreditRange(newValue);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchRegions();
        const regions = response.data;
        setRegions(regions);
      } catch (err) {
      }

      try {
        const response = await fetchTypes();
        const types = response.data;
        setTypes(types);
      } catch (err) {
      }

      try {
        const response = await fetchSpaceRange();
        var spaceRange = [0, 100];
        if (response.data.min != null) {
          spaceRange[0] = response.data.min;
          setSpaceMin(response.data.min);
        }
        if (response.data.max != null) {
          spaceRange[1] = response.data.max;
          setSpaceMax(response.data.max);
        }
        setSpaceRange(spaceRange);
      } catch (err) {
      }

      try {
        const response = await fetchRentRange();
        var rentRange = [0, 10000];
        if (response.data.min != null) {
          rentRange[0] = response.data.min;
          setRentMin(response.data.min);
        }
        if (response.data.max != null) {
          rentRange[1] = response.data.max;
          setRentMax(response.data.max);
        }
        setRentRange(rentRange);
      } catch (err) {
      }

      try {
        const response = await fetchFloorRange();
        var floorRange = [0, 10];
        if (response.data.min != null) {
          floorRange[0] = response.data.min;
          setFloorMin(response.data.min);
        }
        if (response.data.max != null) {
          floorRange[1] = response.data.max;
          setFloorMax(response.data.max);
        }
        setFloorRange(floorRange);
      } catch (err) {
      }

      try {
        const response = await fetchCreditRange();
        var creditRange = [0, 1000];
        if (response.data.min != null) {
          creditRange[0] = response.data.min;
          setCreditMin(response.data.min);
        }
        if (response.data.max != null) {
          creditRange[1] = response.data.max;
          setCreditMax(response.data.max);
        }
        setCreditRange(creditRange);
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
            Living Space (m²)
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Living space range'}
              value={spaceRange}
              onChange={handleSpaceRangeChange}
              valueLabelDisplay="on"
              min={spaceMin}
              max={spaceMax}
              sx={{ mt: 5 }}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="rent">
            Rent (SEK)
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Rent range'}
              value={rentRange}
              onChange={handleRentRangeChange}
              valueLabelDisplay="on"
              min={rentMin}
              max={rentMax}
              sx={{ mt: 5 }}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="floor">
            Floor
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Floor range'}
              value={floorRange}
              onChange={handleFloorRangeChange}
              valueLabelDisplay="on"
              min={floorMin}
              max={floorMax}
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
              min={creditMin}
              max={creditMax}
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

        <FormGrid item xs={12}>
          <FormLabel htmlFor="electricity inlcude">
            Electricity Included
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="June & July Free">
            June & July Freed
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="Max 4 Years">
            Max 4 Years
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="Short Rent">
            Short Rent
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

      </Grid>
    </React.Fragment>
  );
}

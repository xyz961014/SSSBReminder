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

import LoadingBox from './LoadingBox';
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

export default function Filter({ onFilterChange }) {
  const theme = useTheme();

  const [loading, setLoading] = useState(true);

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

  const [electricityIncluded, setEletricityIncluded] = useState("");
  const [summerFree, setSummerFree] = useState("");
  const [max4Years, setMax4Years] = useState("");
  const [shortRent, setShortRent] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          regionsResponse,
          typesResponse,
          spaceRangeResponse,
          rentRangeResponse,
          floorRangeResponse,
          creditRangeResponse,
        ] = await Promise.all([
          fetchRegions(),
          fetchTypes(),
          fetchSpaceRange(),
          fetchRentRange(),
          fetchFloorRange(),
          fetchCreditRange(),
        ]);
  
        const regions = regionsResponse.data;
        setRegions(regions);
  
        const types = typesResponse.data;
        setTypes(types);
  
        const spaceRange = [spaceRangeResponse.data.min || 0, spaceRangeResponse.data.max || 100];
        setSpaceMin(spaceRangeResponse.data.min || 0);
        setSpaceMax(spaceRangeResponse.data.max || 100);
        setSpaceRange(spaceRange);
  
        const rentRange = [rentRangeResponse.data.min || 0, rentRangeResponse.data.max || 10000];
        setRentMin(rentRangeResponse.data.min || 0);
        setRentMax(rentRangeResponse.data.max || 10000);
        setRentRange(rentRange);
  
        const floorRange = [floorRangeResponse.data.min || 0, floorRangeResponse.data.max || 10];
        setFloorMin(floorRangeResponse.data.min || 0);
        setFloorMax(floorRangeResponse.data.max || 10);
        setFloorRange(floorRange);
  
        const creditRange = [creditRangeResponse.data.min || 0, creditRangeResponse.data.max || 1000];
        setCreditMin(creditRangeResponse.data.min || 0);
        setCreditMax(creditRangeResponse.data.max || 1000);
        setCreditRange(creditRange);
  
      } catch (err) {
        // console.error('Error fetching data:', err);
      } finally {
        setLoading(false); 
      }
    };
  
    fetchData();
  }, []);

 useEffect(() => {
   if (onFilterChange) {
     onFilterChange({
       selectedRegion,
       selectedType,
       spaceRange,
       rentRange,
       floorRange,
       creditRange,
       electricityIncluded,
       summerFree,
       max4Years,
       shortRent
     });
    }
  }, [
    selectedRegion,
    selectedType,
    spaceRange,
    rentRange,
    floorRange,
    creditRange,
    electricityIncluded,
    summerFree,
    max4Years,
    shortRent,
    onFilterChange
  ]);

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
      <LoadingBox loading={loading}>
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
              displayEmpty
              value={selectedRegion}
              onChange={handleRegionChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                selected.length === 0 ? (
                  <em>Not Specified</em>
                ) : (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              <MenuItem disabled value="">
                <em>Not Specified</em>
              </MenuItem>
              {regions.map((region) => (
                <MenuItem
                  key={region}
                  value={region}
                >
                  {region}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}} onClick={() => {setSelectedRegion([])}}>
              Clear All
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
              displayEmpty
              value={selectedType}
              onChange={handleTypeChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                selected.length === 0 ? (
                  <em>Not Specified</em>
                ) : (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              <MenuItem disabled value="">
                <em>Not Specified</em>
              </MenuItem>
              {types.map((type) => (
                <MenuItem
                  key={type}
                  value={type}
                >
                  {type}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}} onClick={() => {setSelectedType([]);}}>
              Clear All
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
              onChange={(e) => setSpaceRange(e.target.value)}
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
              onChange={(e) => setRentRange(e.target.value)}
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
              onChange={(e) => setFloorRange(e.target.value)}
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
              onChange={(e) => setCreditRange(e.target.value)}
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
              value={electricityIncluded}
              onChange={(e) => setEletricityIncluded(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="June & July Free">
            June & July Free
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
              value={summerFree}
              onChange={(e) => setSummerFree(e.target.value)}
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
              value={max4Years}
              onChange={(e) => setMax4Years(e.target.value)}
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
              value={shortRent}
              onChange={(e) => setShortRent(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

      </Grid>
      </LoadingBox>
    </React.Fragment>
  );
}

import * as React from 'react';
import dayjs from 'dayjs';
import { useEffect, useState } from 'react';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid';
import OutlinedInput from '@mui/material/OutlinedInput';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import Switch from '@mui/material/Switch';
import EditIcon from '@mui/icons-material/Edit';
import CancelIcon from '@mui/icons-material/Cancel';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/system';

import LoadingBox from './LoadingBox';
import Descriptions from './Descriptions';
import LocalDatePicker from './LocalDatePicker';
import SuccessSnackbar from './SimpleSnackbar';
import MultipleSelectChip from './MultiSelectShip';
import { fetchRegions, fetchTypes } from '../../Api'
import { fetchSpaceRange, fetchRentRange, fetchFloorRange, fetchCreditRange } from '../../Api'
import { fetchFilterData, unsubscribeFilter } from '../../Api';
import { editFilter } from '../../Api'

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

export default function EditFilter({ filterId, onFilterChange }) {
  const theme = useTheme();

  const [loading, setLoading] = useState(true);
  const [active, setActive] = useState(true);

  const [spaceUnspecified, setSpaceUnspecified] = useState(false);
  const [rentUnspecified, setRentUnspecified] = useState(false);
  const [floorUnspecified, setFloorUnspecified] = useState(false);
  const [creditUnspecified, setCreditUnspecified] = useState(false);

  const [regions, setRegions] = useState([]);
  const [types, setTypes] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState([]);
  const [selectedType, setSelectedType] = useState([]);

  const [address, setAddress] = useState(null);

  const [spaceMin, setSpaceMin] = useState(0);
  const [spaceMax, setSpaceMax] = useState(200);
  const [spaceRange, setSpaceRange] = useState([0, 200]);

  const [rentMin, setRentMin] = useState(0);
  const [rentMax, setRentMax] = useState(25000);
  const [rentRange, setRentRange] = useState([0, 25000]);

  const [floorMin, setFloorMin] = useState(-10);
  const [floorMax, setFloorMax] = useState(50);
  const [floorRange, setFloorRange] = useState([-10, 50]);

  const [electricityIncluded, setEletricityIncluded] = useState("");
  const [summerFree, setSummerFree] = useState("");
  const [max4Years, setMax4Years] = useState("");
  const [shortRent, setShortRent] = useState("");

  // for reminder
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const [credit, setCredit] = useState("");
  const [successSnackbarOpen, setSuccessSnackbarOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchFilterData(filterId);
        if (response.data && response.data.length > 0) {
          const filterData = response.data[0];
          // console.log(filterData);
          setSelectedRegion(filterData.regions);
          setSelectedType(filterData.types);
          setAddress(filterData.address);
          if (filterData.living_space) {
            setSpaceRange([filterData.living_space.min, filterData.living_space.max]);
          } else {
            setSpaceUnspecified(true);
          }
          if (filterData.rent) {
            setRentRange([filterData.rent.min, filterData.rent.max]);
          } else {
            setRentUnspecified(true);
          }
          if (filterData.floor) {
            setFloorRange([filterData.floor.min, filterData.floor.max]);
          } else {
            setFloorUnspecified(true);
          }
          setEletricityIncluded(filterData.electricity_include !== null ? (filterData.electricity_include ? 'true' : 'false') : '');
          setSummerFree(filterData.rent_free_june_and_july !== null ? (filterData.rent_free_june_and_july ? 'true' : 'false') : '');
          setMax4Years(filterData.max_4_years !== null ? (filterData.max_4_years ? 'true' : 'false') : '');
          setShortRent(filterData.short_rent !== null ? (filterData.short_rent ? 'true' : 'false') : '');

          setEmail(filterData.email);
          setCredit(filterData.current_credit);
          setActive(filterData.active);


        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (filterId) {
      fetchData();
    }

  }, [filterId]);


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
        regions.sort((ra, rb) => {
          if (ra > rb) return 1;
          if (ra < rb) return -1;
          return 0;
        })
        setRegions(regions);
  
        const types = typesResponse.data;
        types.sort((ta, tb) => {
          if (ta > tb) return 1;
          if (ta < tb) return -1;
          return 0;
        })
        setTypes(types);
 
      } catch (err) {
        // console.error('Error fetching data:', err);
      } finally {
      }
    };
  
    fetchData();
  }, []);

 useEffect(() => {
   if (onFilterChange && !loading) {
     onFilterChange({
       selectedRegion,
       selectedType,
       address,
       spaceRange,
       rentRange,
       floorRange,
       spaceUnspecified,
       rentUnspecified,
       floorUnspecified,
       creditUnspecified,
       electricityIncluded,
       summerFree,
       max4Years,
       shortRent,
     });
    }
  }, [
    selectedRegion,
    selectedType,
    address,
    spaceRange,
    rentRange,
    floorRange,
    spaceUnspecified,
    rentUnspecified,
    floorUnspecified,
    creditUnspecified,
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

  const handleEditReminder = async () => {
    try {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      setError(!emailRegex.test(email));
      if (!error) {
        const filterDict = {
          "filter_id": filterId,
          "email": email,
          "regions": selectedRegion,
          "types": selectedType,
          "address": address,
          "living_space": spaceUnspecified ? null : {
            "min": spaceRange[0],
            "max": spaceRange[1],
          },
          "rent": rentUnspecified ? null : {
            "min": rentRange[0],
            "max": rentRange[1],
          },
          "floor": floorUnspecified ? null : {
            "min": floorRange[0],
            "max": floorRange[1],
          },
          "electricity_include": electricityIncluded !== "" ? electricityIncluded === "true" : null,
          "rent_free_june_and_july": summerFree !== "" ? summerFree === "true" : null,
          "max_4_years": max4Years !== "" ? max4Years === "true" : null,
          "short_rent": shortRent !== "" ? shortRent === "true" : null,
          "current_credit": credit,
        };
        // console.log(filterDict)
        setDialogLoading(true);
        const response = await editFilter(filterDict);
        setDialogLoading(false);
        setDialogOpen(false);
        setSuccessSnackbarOpen(true);
        setTimeout(() => {
          setSuccessSnackbarOpen(false);
        }, 6000);
      }
    } catch (error) {
        console.error('failed', error);
    }
  };

  const handleUnsubscribe = () => {
    const unsubscribe = async () => {
      try {
        setLoading(true);
        const response = await unsubscribeFilter(filterId);
        if (response.data && response.data.success) {
          setActive(false);
        }
      }
      catch {
      }
      finally {
        setLoading(false);
      }
    }
    if (filterId) {
      unsubscribe();
    }
  };

  return (
    <React.Fragment>
      <LoadingBox loading={loading}>
      <Grid container spacing={2}>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="space">
            Reminder Email: {email}
          </FormLabel>
        </FormGrid>
        <FormGrid item xs={12}>
          <FormLabel htmlFor="space">
            Credit Days: {credit}
          </FormLabel>
        </FormGrid>

        <FormGrid item xs={12}>
          <Box sx={{ display: 'flex', mb: 2, gap: 2 }}>
            <Button
              variant="outlined"
              color="error"
              startIcon={<CancelIcon />}
              onClick={handleUnsubscribe}
              disabled={!active}
            >
              Unsubscribe
            </Button>
            <Button
              variant="outlined"
              startIcon={<EditIcon />}
              onClick={() => setDialogOpen(true)}
              disabled={!active}
            >
              Edit Reminder
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'nowrap', gap: 2 }}>
            <MultipleSelectChip
              label='Region'
              options={regions}
              value={selectedRegion}
              onValueChange={(v) => setSelectedRegion(v)}
              width="100%"
              disabled={!active}
            />

            <Button 
              variant="text" 
              sx={{ whiteSpace: 'nowrap', flexShrink: 0 }} 
              onClick={() => {setSelectedRegion([])}}
              disabled={!active}
            >
              Clear All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'nowrap', gap: 2 }}>

            <MultipleSelectChip
              label='Accomodation Type'
              options={types}
              value={selectedType}
              onValueChange={(v) => setSelectedType(v)}
              width="100%"
              disabled={!active}
            />
            <Button 
              variant="text" 
              sx={{ whiteSpace: 'nowrap', flexShrink: 0 }} 
              onClick={() => {setSelectedType([]);}}
              disabled={!active}
            >
              Clear All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <TextField
                margin="dense"
                label="Address"
                value={address ? address : ""}
                fullWidth
                onChange={(e) => setAddress(e.target.value)}
                disabled={!active}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="space">
            Living Space (m²)
            <FormControlLabel 
              control={
                <Switch 
                  checked={spaceUnspecified}
                  onChange={(e) => setSpaceUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                  disabled={!active}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />
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
              disabled={spaceUnspecified || !active}
            />

          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="rent">
            Monthly Rent (SEK)

            <FormControlLabel 
              control={
                <Switch 
                  checked={rentUnspecified}
                  onChange={(e) => setRentUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                  disabled={!active}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />

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
              disabled={rentUnspecified || !active}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="floor">
            Floor
            <FormControlLabel 
              control={
                <Switch 
                  checked={floorUnspecified}
                  onChange={(e) => setFloorUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                  disabled={!active}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />
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
              disabled={floorUnspecified || !active}
            />
          </Box>
        </FormGrid>

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
              <FormControlLabel value={true} control={<Radio />} label="Yes" disabled={!active} />
              <FormControlLabel value={false} control={<Radio />} label="No" disabled={!active} />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" disabled={!active} />
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
              <FormControlLabel value={true} control={<Radio />} label="Yes" disabled={!active} />
              <FormControlLabel value={false} control={<Radio />} label="No" disabled={!active} />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" disabled={!active} />
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
              <FormControlLabel value={true} control={<Radio />} label="Yes" disabled={!active} />
              <FormControlLabel value={false} control={<Radio />} label="No" disabled={!active} />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" disabled={!active} />
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
              <FormControlLabel value={true} control={<Radio />} label="Yes" disabled={!active}/>
              <FormControlLabel value={false} control={<Radio />} label="No" disabled={!active}/>
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" disabled={!active}/>
            </RadioGroup>
          </Box>
        </FormGrid>


      </Grid>
      </LoadingBox>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} fullWidth>
        <LoadingBox loading={dialogLoading}>
          <DialogTitle>Edit Reminder</DialogTitle>
          <DialogContent>
              <DialogContentText>
                Please enter your email address
              </DialogContentText>
              <TextField
                  autoFocus
                  margin="dense"
                  label="Email address"
                  type="email"
                  fullWidth
                  value={email}
                  error={error}
                  helperText={error ? "Please enter a valid email" : ""}
                  onChange={(e) => setEmail(e.target.value)}
              />
              <DialogContentText>
                Please enter your current credit days
              </DialogContentText>
              <TextField
                  margin="dense"
                  label="Credit days"
                  type="number"
                  fullWidth
                  value={credit}
                  onChange={(e) => setCredit(e.target.value)}
              />
              <DialogContentText>
                Your personal filter
              </DialogContentText>
              <Box sx={{ mt: 1 }}>
                <Descriptions 
                  items={[
                    {
                      "label": "Region",
                      "value": selectedRegion.length > 0 ? selectedRegion.join(", ") : "Not Specified",
                    },
                    {
                      "label": "Accomodation Type",
                      "value": selectedType.length > 0 ? selectedType.join(", ") : "Not Specified",
                    },
                    {
                      "label": "Address",
                      "value": address && address.length > 0 ? address : "Not Specified",
                    },
                    {
                      "label": "Living Space",
                      "value": !spaceUnspecified ? `${spaceRange[0]} m² ~ ${spaceRange[1]} m²` : "Not Specified",
                    },
                    {
                      "label": "Monthly Rent",
                      "value": !rentUnspecified ? `${rentRange[0]} SEK ~ ${rentRange[1]} SEK` : "Not Specified",
                    },
                    {
                      "label": "Floor",
                      "value": ! floorUnspecified ? `${floorRange[0]} ~ ${floorRange[1]}`: "Not Specified",
                    },
                    {
                      "label": "Current Credit Days",
                      "value": credit ? `${credit} days`: "Not Specified",
                    },
                    {
                      "label": "Electricity Included",
                      "value": electricityIncluded === "" ? `Not Specified`: (electricityIncluded === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "June & July Free",
                      "value": summerFree === "" ? `Not Specified`: (summerFree === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "Max 4 Years",
                      "value": max4Years === "" ? `Not Specified`: (max4Years === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "Short Rent",
                      "value": shortRent === "" ? `Not Specified`: (shortRent === "true" ? "Yes": "No"),
                    },
                  ]} 
                  column={3} 
                />
              </Box>
          </DialogContent>
          <DialogActions>
              <Button onClick={() => setDialogOpen(false)} color="error">
                  Cancel
              </Button>
              <Button onClick={handleEditReminder} color="primary">
                  Confirm
              </Button>
          </DialogActions>
        </LoadingBox>
      </Dialog>

      <SuccessSnackbar 
        open={successSnackbarOpen}
        message="Filter edited successfully. Please check your email for details."
      />


    </React.Fragment>
  );
}

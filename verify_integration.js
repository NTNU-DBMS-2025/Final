#!/usr/bin/env node
/**
 * Frontend Integration Verification Script
 * Checks API imports and configurations without requiring backend
 */

const fs = require('fs');
const path = require('path');

// Configuration
const FRONTEND_DIR = './frontend/src/api';
const expectedAPIFiles = [
    'axios.js',
    'auth.js',
    'products.js',
    'suppliers.js',
    'customers.js',
    'orders.js',
    'inventory.js',
    'locations.js',
    'shipments.js',
    'scrap.js',
    'users.js'
];

function checkFileExists(filePath) {
    return fs.existsSync(filePath);
}

function checkAPIFiles() {
    console.log('📁 Checking API Files...\n');

    let allFilesExist = true;

    expectedAPIFiles.forEach(file => {
        const filePath = path.join(FRONTEND_DIR, file);
        const exists = checkFileExists(filePath);

        if (exists) {
            console.log(`✅ ${file} - Found`);
        } else {
            console.log(`❌ ${file} - Missing`);
            allFilesExist = false;
        }
    });

    return allFilesExist;
}

function checkAxiosConfig() {
    console.log('\n🔧 Checking Axios Configuration...\n');

    const axiosPath = path.join(FRONTEND_DIR, 'axios.js');

    if (!checkFileExists(axiosPath)) {
        console.log('❌ axios.js not found');
        return false;
    }

    const content = fs.readFileSync(axiosPath, 'utf8');

    // Check base URL
    if (content.includes('http://localhost:5001')) {
        console.log('✅ Base URL correctly set to http://localhost:5001');
    } else {
        console.log('❌ Base URL not set to http://localhost:5001');
        return false;
    }

    // Check credentials
    if (content.includes('withCredentials: true')) {
        console.log('✅ withCredentials enabled for session support');
    } else {
        console.log('❌ withCredentials not enabled');
        return false;
    }

    return true;
}

function checkAPIExports() {
    console.log('\n📦 Checking API Exports...\n');

    const apiChecks = [
        { file: 'orders.js', exports: ['fetchOrders', 'getOrders', 'createOrder'] },
        { file: 'customers.js', exports: ['fetchCustomers', 'createCustomer'] },
        { file: 'shipments.js', exports: ['fetchShipments', 'createShipment'] },
        { file: 'scrap.js', exports: ['fetchScrapRecords', 'createScrapRecord'] },
        { file: 'locations.js', exports: ['fetchLocations', 'createLocation'] },
        { file: 'users.js', exports: ['fetchUsers', 'fetchRoles'] }
    ];

    let allExportsValid = true;

    apiChecks.forEach(({ file, exports }) => {
        const filePath = path.join(FRONTEND_DIR, file);

        if (!checkFileExists(filePath)) {
            console.log(`❌ ${file} - File not found`);
            allExportsValid = false;
            return;
        }

        const content = fs.readFileSync(filePath, 'utf8');

        exports.forEach(exportName => {
            if (content.includes(`export function ${exportName}`) ||
                content.includes(`${exportName}:`)) {
                console.log(`  ✅ ${file} - ${exportName} export found`);
            } else {
                console.log(`  ❌ ${file} - ${exportName} export missing`);
                allExportsValid = false;
            }
        });
    });

    return allExportsValid;
}

function checkBackendConnections() {
    console.log('\n🔗 Checking Backend Connection Patterns...\n');

    const patterns = [
        { pattern: 'apiClient.get', description: 'GET requests' },
        { pattern: 'apiClient.post', description: 'POST requests' },
        { pattern: 'apiClient.put', description: 'PUT requests' },
        { pattern: 'apiClient.delete', description: 'DELETE requests' }
    ];

    let patternsFound = 0;

    expectedAPIFiles.forEach(file => {
        const filePath = path.join(FRONTEND_DIR, file);

        if (!checkFileExists(filePath)) return;

        const content = fs.readFileSync(filePath, 'utf8');

        patterns.forEach(({ pattern, description }) => {
            if (content.includes(pattern)) {
                patternsFound++;
            }
        });
    });

    if (patternsFound > 0) {
        console.log(`✅ Found ${patternsFound} backend API calls across all files`);
        return true;
    } else {
        console.log('❌ No backend API calls found');
        return false;
    }
}

function generateSummary(results) {
    console.log('\n' + '='.repeat(60));
    console.log('📊 Frontend Integration Verification Summary');
    console.log('='.repeat(60));

    const checks = [
        { name: 'API Files', result: results.apiFiles },
        { name: 'Axios Config', result: results.axiosConfig },
        { name: 'API Exports', result: results.apiExports },
        { name: 'Backend Connections', result: results.backendConnections }
    ];

    checks.forEach(({ name, result }) => {
        const status = result ? '✅ PASS' : '❌ FAIL';
        console.log(`${name}: ${status}`);
    });

    const allPassed = Object.values(results).every(result => result);

    console.log(`\nOverall Status: ${allPassed ? '✅ ALL CHECKS PASSED' : '❌ SOME CHECKS FAILED'}`);

    if (allPassed) {
        console.log('\n🎉 Frontend is ready for backend integration!');
        console.log('Next steps:');
        console.log('1. Start the backend server: cd backend && python app.py');
        console.log('2. Start the frontend server: cd frontend && npm run dev');
        console.log('3. Run integration test: python test_integration.py');
    } else {
        console.log('\n🔧 Please fix the failing checks before proceeding.');
    }

    return allPassed;
}

function main() {
    console.log('🧪 Frontend Integration Verification\n');

    const results = {
        apiFiles: checkAPIFiles(),
        axiosConfig: checkAxiosConfig(),
        apiExports: checkAPIExports(),
        backendConnections: checkBackendConnections()
    };

    const success = generateSummary(results);
    process.exit(success ? 0 : 1);
}

// Run the verification
main(); 